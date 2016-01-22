# coding: utf-8
from os import path, curdir
import unittest
import schemaprobe

DOCS_DIR = path.join(path.abspath(path.dirname(__file__)), '../docs/v1')
ARTICLE_DOCS = path.abspath(path.join(DOCS_DIR, 'article'))


class TestArticle(unittest.TestCase):

    def setUp(self):
        self.sample = open(path.join(ARTICLE_DOCS, 'sample.json'), 'r')
        self.schema = open(path.join(ARTICLE_DOCS, 'schema.json'), 'r')

    def tearDown(self):
        self.sample.close()
        self.schema.close()

    def test_article_sample_is_valid(self):
        '''
        validação do sample (docs/article/sample.json)
        contra o schema (docs/article/schema.json)
        '''
        probe = schemaprobe.JsonProbe(self.schema.read())
        self.assertTrue(probe.validate(self.sample.read()))
