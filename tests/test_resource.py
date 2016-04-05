# coding: utf-8
from os import path, curdir
import unittest
import schemaprobe

DOCS_DIR = path.join(path.abspath(path.dirname(__file__)), '../docs/v1')
RESOURCE_DOCS = path.abspath(path.join(DOCS_DIR, 'resource'))


class TestResource(unittest.TestCase):

    def setUp(self):
        self.sample = open(path.join(RESOURCE_DOCS, 'sample.json'), 'r')
        self.schema = open(path.join(RESOURCE_DOCS, 'schema.json'), 'r')

    def tearDown(self):
        self.sample.close()
        self.schema.close()

    def test_resource_sample_is_valid(self):
        '''
        validação do sample (docs/resource/sample.json)
        contra o schema (docs/resource/schema.json)
        '''
        probe = schemaprobe.JsonProbe(self.schema.read())
        self.assertTrue(probe.validate(self.sample.read()))
