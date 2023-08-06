import os
import datetime
import logging
import json
import uuid
import unicodedata
import hashlib
import base64
import traceback

from azure.storage.queue import QueueClient
from azure.storage.blob import BlobClient
from azure.cosmosdb.table import TableService

enough_workers_message = "There are already enough active workers"
workers_long_running = "Workers are active for too long. Going to process as well."
state_table = "workerState"
failure_table = "executionFailures"
wake_up_queue_name = "wake-up"

input_container = "input"
output_container = "output"


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class Worker:
    def __init__(self, queue_name, metadata_table_name, worker_name, should_wake_up=False, segment_limit=1000, batch_size=100):
        connection_string = os.environ['AzureWebJobsStorage']
        self.metadata_table_name = metadata_table_name
        self.table_client = TableService(connection_string=connection_string)
        self.queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=queue_name)
        if should_wake_up:
            self.wake_up_queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=wake_up_queue_name)
        self.should_wake_up = should_wake_up
        self.worker_name = worker_name
        if 'LtbCloudComponentsStorage' in os.environ:
            self.ltb_connection_string = os.environ['LtbCloudComponentsStorage']
        else:
            self.ltb_connection_string = None
        self.segment_limit = segment_limit
        self.batch_size = batch_size

    def trigger_blob(self, blob_name, data=None):
        request_id = self._insert_blob_metadata(blob_name, data)
        self._enqueue(request_id)
        self._wake_up()
        return request_id

    def trigger(self, data):
        request_id = self._insert_request_metadata(data)
        self._enqueue(request_id)
        self._wake_up()
        return request_id

    def process_messages_stateful(self, func, blob_func=None):
        state_row = list(self.table_client.query_entities(state_table))[0]
        now = datetime.datetime.now(datetime.timezone.utc)
        active_count = state_row['ActiveCount'].value
        max_count = state_row['MaxCount'].value
        if active_count >= max_count:
            logging.info(enough_workers_message)
            diff = now - state_row['UpdateDate']
            if diff.total_seconds() > 300:
                logging.info(workers_long_running)
            else:
                return
        else:
            state_row['ActiveCount'].value += 1
            state_row['UpdateDate'] = now
            self.table_client.update_entity(state_table, state_row)

        try:
            while True:
                response = self.queue.receive_messages(messages_per_page=32)
                messages = list(response)
                logging.info(str(len(messages)))
                if len(messages) == 0:
                    break
                for message in messages:
                    content = base64.b64decode(message.content).decode("utf-8")
                    self.process_message(content, func, blob_func)
                    self.queue.delete_message(message)
        finally:
            state_row['ActiveCount'].value = 0
            state_row['UpdateDate'] = datetime.datetime.now(datetime.timezone.utc)
            self.table_client.update_entity(state_table, state_row)

    def process_message(self, request_id, func, blob_func=None):
        try:
            guid, request_hash = self._decode_id(request_id)
            request_entity = self.table_client.get_entity(self.metadata_table_name, guid, request_hash)
            if 'Request' in request_entity:
                self._process_request_body(request_entity, func)
            if 'BlobName' in request_entity:
                self._process_blob(request_id, request_entity, blob_func)
        except Exception as e:
            self._record_request_failure(request_entity, e)
            if self.ltb_connection_string is not None:
                self._record_failure(request_id, e)
            else:
                raise

    def _process_blob(self, request_id, request_entity, func):
        blob_name, params, offset, retry_count, batch_count = self._read_metadata(request_entity)
        try:
            result, whole_blob_read = self._process_blob_by_segments(blob_name, func, offset, params)
        except Exception as e:
            if retry_count == 3:
                self._record_failure(request_id, e)
            else:
                request_entity['RetryCount'] = retry_count + 1
                self.table_client.update_entity(self.metadata_table_name, request_entity)
                self._enqueue(request_id)
            return
            
        serialized_result = "\n".join(json.dumps(r) for r in result)
        if not whole_blob_read:
            out_blob = self._get_output_blob("%s/%s_%d" % (self.worker_name, blob_name, batch_count))
            out_blob.upload_blob(serialized_result, timeout=1200)
                
            request_entity['Offset'] = offset + len(result)
            request_entity['Batch'] = batch_count + 1
            self.table_client.update_entity(self.metadata_table_name, request_entity)
            self._enqueue(request_id)
        else:
            out_blob = self._get_output_blob("%s/%s" % (self.worker_name, blob_name))
            if offset == 0:
                out_blob.upload_blob(serialized_result, timeout=1200)
            else:     
                content = []
                for batch in range(batch_count):
                    in_blob = self._get_output_blob("%s/%s_%d" % (self.worker_name, blob_name, batch))
                    blob_content = in_blob.download_blob().readall().decode()
                    content.append(blob_content)
                content.append(serialized_result)
                out_blob.upload_blob("\n".join(content), timeout=1200)

    def _get_input_blob(self, blob_name):
        return BlobClient.from_connection_string(self.ltb_connection_string, container_name=input_container, blob_name=blob_name)

    def _get_output_blob(self, blob_name):
        return BlobClient.from_connection_string(self.ltb_connection_string, container_name=output_container, blob_name=blob_name)

    def _read_metadata(self, request_entity):
        blob_name = request_entity['BlobName']
        params = None
        if 'Parameters' in request_entity:
            params = json.loads(request_entity['Parameters'])
        offset = 0
        if 'Offset' in request_entity:
            offset = request_entity['Offset']
        retry_count = 0
        if 'RetryCount' in request_entity:
            retry_count = request_entity['RetryCount']
        batch_count = 0
        if 'Batch' in request_entity:
            batch_count = request_entity['Batch']
        return blob_name, params, offset, retry_count, batch_count

    def _process_blob_by_segments(self, blob_name, func, offset, params):
        result = []
        in_blob = self._get_input_blob(blob_name)
        batch = []
        segment_id = -1
        whole_blob_read = True
        for source_segment in self._read_blob_by_segments(in_blob):
            segment_id += 1
            if segment_id < offset:
                continue

            batch.append(source_segment)
            if len(batch) == self.batch_size:
                result.extend(func(batch, params))
                batch = []

            if segment_id - offset + 1 >= self.segment_limit:
                whole_blob_read = False
                break

        if len(batch) > 0:
            result.extend(func(batch, params))
            
        return result, whole_blob_read

    def _record_failure(self, request_id, e: Exception):
        track = traceback.format_exc()
        function_failure_entity = {"PartitionKey": self.worker_name, "RowKey": request_id, "FailureMessage": str(e), "StackTrace": track}
        TableService(connection_string=self.ltb_connection_string).insert_entity(failure_table, function_failure_entity)

    def _record_request_failure(self, request_entity, e: Exception):
        trace = traceback.format_exc()
        error_message = str(e)
        request_entity['Error'] = error_message
        request_entity['StackTrace'] = trace
        self.table_client.update_entity(self.metadata_table_name, request_entity)
        
    def get_result(self, request_id):
        guid, request_hash = self._decode_id(request_id)
        entity = self.table_client.get_entity(self.metadata_table_name, guid, request_hash)
        if 'Result' not in entity:
            return ""
        return entity['Result']

    def _insert_request_metadata(self, data):
        serialized_body = json.dumps(data)
        guid, request_hash, request_id = self._generate_id(serialized_body)
        metadata = {"PartitionKey": guid, "RowKey": request_hash, "Request": serialized_body }
        self.table_client.insert_entity(self.metadata_table_name, metadata)
        return request_id

    def _insert_blob_metadata(self, blob_name, data=None):
        guid, request_hash, request_id = self._generate_id(blob_name)
        metadata_entity = {"PartitionKey": guid, "RowKey": request_hash, "BlobName": blob_name}
        if data:
            metadata_entity['Parameters'] = json.dumps(data)
        self.table_client.insert_entity(self.metadata_table_name, metadata_entity)
        return request_id

    def _enqueue(self, request_id):
        self.queue.send_message(base64.b64encode(request_id.encode()).decode())

    def _process_request_body(self, request_entity, func):
        if 'Request' not in request_entity:
            return
        request_body = json.loads(request_entity['Request'])
        response = func(request_body)
        request_entity['Result'] = json.dumps(response)
        self.table_client.update_entity(self.metadata_table_name, request_entity)

    def _wake_up(self):
        if self.should_wake_up:
            self.wake_up_queue.send_message("d2FrZSB1cA==")

    @staticmethod
    def _read_blob_by_chunks(input_blob):
        blob_data = input_blob.download_blob()
        last_piece = ""
        for chunk in blob_data.chunks():
            lines = [l.strip() for l in chunk.decode().split("\r\n") if len(l.strip()) > 0]
            lines[0] = last_piece + lines[0]
            last_piece = lines[-1]
            source_segments = []
            for l in lines[:-1]:
                l = unicodedata.normalize("NFKD", l).strip()
                if len(l) == 0:
                    continue
                source_segment = json.loads(l)[0].strip()
                source_segments.append(source_segment)
            yield source_segments

        last_piece = unicodedata.normalize("NFKD", last_piece).strip()
        if len(last_piece) > 0:
            source = None
            try:
                source = json.loads(last_piece)[0].strip()
            except:
                pass
            if source:
                yield [source]

    @staticmethod
    def _read_blob_by_segments(input_blob):
        blob_data = input_blob.download_blob()
        last_piece = ""
        for chunk in blob_data.chunks():
            lines = [l.strip() for l in chunk.decode().split("\r\n") if len(l.strip()) > 0]
            lines[0] = last_piece + lines[0]
            last_piece = lines[-1]
            for l in lines[:-1]:
                l = unicodedata.normalize("NFKD", l).strip()
                if len(l) == 0:
                    continue
                source_segment = json.loads(l)[0].strip()
                yield source_segment

        last_piece = unicodedata.normalize("NFKD", last_piece).strip()
        if len(last_piece) > 0:
            source = None
            try:
                source = json.loads(last_piece)[0].strip()
            except:
                pass
            if source:
                yield source

    @staticmethod
    def _generate_id(data):
        request_id = str(uuid.uuid4()).replace("-", "")
        request_hash = str(hashlib.md5(data.encode()).hexdigest())
        response = "%s_%s" % (request_id, request_hash)
        return request_id, request_hash, response
    
    @staticmethod
    def _decode_id(request_id):
        guid, request_hash = request_id.split("_")
        return guid, request_hash
