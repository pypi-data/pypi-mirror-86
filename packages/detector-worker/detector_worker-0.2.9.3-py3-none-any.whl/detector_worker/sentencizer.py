import spacy


class SpacySentencizer:
    def __init__(self):
        spacy.cli.download('en_core_web_sm')
        self.model = spacy.load('en_core_web_sm', disable=['ner'])

    def split_into_sentences(self, text):
        sentences = [str(s).strip() for s in self.model(text).sents]
        return sentences