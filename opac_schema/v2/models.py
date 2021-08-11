# coding: utf-8
from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    # campos:
    StringField,
    DateTimeField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    URLField,
    DictField,
)


class RemoteAndLocalFile(EmbeddedDocument):
    """
    Armazena URI, nome do arquivo e anotações sobre o arquivo
    """
    uri = URLField(required=True)
    name = StringField(required=True)
    annotation = DictField()

    def __unicode__(self):
        return '%s' % self.name


class ReceivedPackage(Document):
    """
    Armazena URI, nome do arquivo e anotações sobre o zip recebido
    """
    _id = StringField(max_length=32, primary_key=True, required=True)
    file = EmbeddedDocumentField(RemoteAndLocalFile)
    created = DateTimeField()
    updated = DateTimeField()
    meta = {
        'collection': 'received_pkg',
        'indexes': ['created'],
    }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        self.updated = datetime.now()

    def __unicode__(self):
        return '%s' % self.file and self.file.name


class ArticleFiles(Document):
    """
    Armazena
    - xml com URI e nome
    - renditions com respectivos URI e nome
    - assets com respectivos URI e nome
    - zip para download com respectivos URI, nome do arquivo e anotações
    """
    _id = StringField(max_length=32, primary_key=True, required=True)
    file = EmbeddedDocumentField(RemoteAndLocalFile)
    created = DateTimeField()
    updated = DateTimeField()

    xml = EmbeddedDocumentField(RemoteAndLocalFile)
    renditions = EmbeddedDocumentListField(RemoteAndLocalFile)
    assets = EmbeddedDocumentListField(RemoteAndLocalFile)

    meta = {
        'collection': 'article_files',
        'indexes': ['updated', 'xml'],
    }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        self.updated = datetime.now()

    def __unicode__(self):
        return '%s %s' % (self._id, self.xml and self.xml.name)
