# coding: utf-8
from os import path, curdir
import unittest
import schemaprobe

DOCS_DIR = path.join(path.abspath(path.dirname(__file__)), '../docs/v1')
JOURNAL_DOCS = path.abspath(path.join(DOCS_DIR, 'journal'))


class TestJournal(unittest.TestCase):

    def setUp(self):
        self.sample = open(path.join(JOURNAL_DOCS, 'sample.json'), 'r')
        self.schema = open(path.join(JOURNAL_DOCS, 'schema.json'), 'r')

    def tearDown(self):
        self.sample.close()
        self.schema.close()

    def test_journal_sample_is_valid(self):
        '''
        validação do sample (docs/journal/sample.json)
        contra o schema (docs/journal/schema.json)
        '''
        probe = schemaprobe.JsonProbe(self.schema.read())
        self.assertTrue(probe.validate(self.sample.read()))

if __name__ == '__main__':
    unittest.main()
