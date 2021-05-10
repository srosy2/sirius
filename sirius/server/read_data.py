import docx
import os
import re
import pathlib


class TextData:
    def __init__(self, path: str):
        self.path = "/".join([str(pathlib.Path().absolute()), path])
        # self.path = "/home/sirius/DELETEME/sirius/server/uploads/current/"
        self.topic_text = dict()

    def _load_name_file_doc(self):
        # path = "/home/sirius/DELETEME/sirius/server/uploads/current/train_data/"
        return sorted(os.listdir(self.path))

    def _prepare_text(self, text):
        text = text.replace('\xa0', ' ')
        text = text.replace(r'\n', ' ')
        return text

    def get_text(self, files=None):
        if files is None:
            files = self._load_name_file_doc()
        else:
            if type(files) == str:
                files = [files]
        for file in files:
            doc = docx.Document(os.path.join(self.path, file))
            full_text = []
            for para in doc.paragraphs:
                # full_text.append(unidecode.unidecode(para.text))
                full_text.append(self._prepare_text(para.text))
            self.topic_text.update({file: ' '.join(full_text).strip(' ')})

    def get_txt_text(self, files=None):
        if files is None:
            files = self._load_name_file_doc()
        else:
            if type(files) == str:
                files = [files]
        for file in files:
            with open(os.path.join(self.path, file), 'r') as read_file:
                doc = read_file.read()
            self.topic_text.update({file: self._prepare_text(doc).strip(' ')})
