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
from azure.cosmosdb.table import TableService, TableBatch

enough_workers_message = "There are already enough active workers"
workers_long_running = "Workers are active for too long. Going to process as well."
state_table = "workerState"
failure_table = "executionFailures"
wake_up_queue_name = "wake-up"

input_container = "input"
output_container = "output"


class TaskResult:
    def __init__(self, result, error_message, stack_trace, offset):
        self.result = result
        self.error_message = error_message
        self.stack_trace = stack_trace
        self.offset = offset

    @staticmethod
    def create_from_request_entity(entity):
        result, error, trace, offset = None, None, None, None
        if 'Result' in entity:
            result = entity['Result']
        if 'Error' in entity:
            error = entity['Error']
        if 'StackTrace' in entity:
            trace = entity['StackTrace']
        if 'Offset' in entity:
            offset = entity['Offset']
        
        return TaskResult(result, error, trace, offset)

    def to_json(self):
        json_response = {"Completed": False}
        if self.result:
            json_response['Result'] = json.loads(self.result)
            json_response['Completed'] = True
        if self.error_message:
            json_response['Error'] = self.error_message
            json_response['StackTrace'] = self.stack_trace
            json_response['Completed'] = True
        if self.offset:
            json_response['Progress'] = self.offset
        return json_response


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

    # There are 3 scenarious:
    # 1. Small blob (under segment_limit size) is being processed. Result is written to the output blob. Task state should be "Completed"
    # 2. Large blob (more than segment_limit) is being processed. Partial result is written to blob_0. Result of blob splitted into segment_list size parts and enqueued.
    # 3. Parent task (with child_task_partition field). We poll child tasks. Record progress. If child task fails -> parent fails as well.
    def _process_blob(self, request_id, request_entity, func):
        blob_name, params, child_task_partition, retry_count = self._read_metadata(request_entity)
        if child_task_partition:
            self._poll_child_tasks(request_entity, request_id, child_task_partition)
            return

        try:
            result, whole_blob_read, blobs_iterator = self._process_blob_by_segments(blob_name, func, params)
        except Exception as e:
            if retry_count == 3:
                self._record_failure(request_id, e)
            else:
                request_entity['RetryCount'] = retry_count + 1
                self.table_client.update_entity(self.metadata_table_name, request_entity)
                self._enqueue(request_id)
            return
        
        serialized_result = "\n".join(json.dumps(r) for r in result)
        if whole_blob_read:
            out_blob = self._get_output_blob("%s/%s" % (self.worker_name, blob_name))
            out_blob.upload_blob(serialized_result, timeout=1200)
            request_entity['State'] = 'Completed'
            self.table_client.update_entity(self.metadata_table_name, request_entity)
        else:
            out_blob = self._get_output_blob("%s/%s_0" % (self.worker_name, blob_name))
            out_blob.upload_blob(serialized_result, timeout=1200)
            blob_names = self._split_blob_into_chunks(blobs_iterator, blob_name)
            partition_key = self._enqueue_child_tasks(blob_names, params)
            request_entity['ChildTasksPartition'] = partition_key
            request_entity['State'] = 'Polling'
            self.table_client.update_entity(self.metadata_table_name, request_entity)
            self._enqueue(request_id)

    def _poll_child_tasks(self, request_entity, request_id, child_tasks_partition):
        completed_blobs = []
        total_count = 0
        for task_entity in self.table_client.query_entities(self.metadata_table_name, filter="PartitionKey eq '%s'" % child_tasks_partition):
            total_count += 1
            if 'State' in task_entity and task_entity['State'] == 'Completed':
                completed_blobs.append(task_entity["BlobName"])
        if len(completed_blobs) == total_count:
            self._merge_blobs(completed_blobs, request_entity["BlobName"])
            request_entity["State"] = "Completed"
            self.table_client.update_entity(self.metadata_table_name, request_entity)
        else:
            request_entity['Progress'] = len(completed_blobs) * self.segment_limit
            self.table_client.update_entity(self.metadata_table_name, request_entity)
            self._enqueue(request_id)

    def _split_blob_into_chunks(self, segment_iterator, blob_name):
        blob_names = []
        batch = []
        batch_number = 1
        for source_segment in segment_iterator:
            batch.append(source_segment)
            if len(batch) == self.segment_limit:
                partial_blob_name = "%s/%s_%d" % (self.worker_name, blob_name, batch_number)
                out_blob = self._get_input_blob(partial_blob_name)
                serialized_result = json.dumps(batch)
                out_blob.upload_blob(serialized_result, timeout=1200)
                blob_names.append(partial_blob_name)
                batch = []
                batch_number += 1
        if len(batch):
            partial_blob_name = "%s/%s_%d" % (self.worker_name, blob_name, batch_number)
            out_blob = self._get_input_blob(partial_blob_name)
            serialized_result = json.dumps(batch)
            out_blob.upload_blob(serialized_result, timeout=1200)
            blob_names.append(partial_blob_name)
        return blob_names

    def _enqueue_child_tasks(self, blob_names, params):
        partition_key = str(uuid.uuid4()).replace("-", "")
        request_hashes = [str(hashlib.md5(data.encode()).hexdigest()) for data in blob_names]
        request_ids = ["%s_%s" % (partition_key, request_hash) for request_hash in request_hashes]
        batch = TableBatch()
        batch_size = 0
        for partial_blob_name, request_hash in zip(blob_names, request_hashes):
            metadata_entity = {"PartitionKey": partition_key, "RowKey": request_hash, "BlobName": partial_blob_name }
            if params:
                metadata_entity['Parameters'] = json.dumps(params)
            batch.insert_entity(metadata_entity)
            batch_size += 1
            if batch_size == 100:
                self.table_client.commit_batch(self.metadata_table_name, batch)
                batch_size = 0
                batch = TableBatch()
                
        if batch_size > 0:
            self.table_client.commit_batch(self.metadata_table_name, batch)

        for child_request_id in request_ids:
            self._enqueue(child_request_id)
        return partition_key

    def _merge_blobs(self, blob_names, blob_name):
        out_blob = self._get_output_blob("%s/%s" % (self.worker_name, blob_names))
        content = []
        for partial_blob_name in sorted(blob_names, key=lambda b: int(b.split('_')[-1])):
            in_blob = self._get_output_blob("%s/%s" % (self.worker_name, partial_blob_name))
            blob_content = in_blob.download_blob().readall().decode()
            content.append(blob_content)
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
        if 'ChildTasksPartition' in request_entity:
            child_tasks_partition = request_entity['ChildTasksPartition']
        retry_count = 0
        if 'RetryCount' in request_entity:
            retry_count = request_entity['RetryCount']
        return blob_name, params, child_tasks_partition, retry_count

    def _process_blob_by_segments(self, blob_name, func, params):
        result = []
        in_blob = self._get_input_blob(blob_name)
        batch = []
        whole_blob_read = True
        segments_processed = 0
        blobs_iterator = self._read_blob_by_segments(in_blob)
        for source_segment in blobs_iterator:
            batch.append(source_segment)
            if len(batch) == self.batch_size:
                result.extend(func(batch, params))
                segments_processed += len(batch)
                batch = []
                if segments_processed >= self.segment_limit:
                    whole_blob_read = False
                    break

        if len(batch) > 0 and whole_blob_read:
            result.extend(func(batch, params))

        return result, whole_blob_read, blobs_iterator

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
        return TaskResult.create_from_request_entity(entity)

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
