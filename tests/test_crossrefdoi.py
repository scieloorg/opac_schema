# coding: utf-8
from mongoengine import ValidationError
from opac_schema.v1.models import CrossrefDOI, Journal
from .base import BaseTestCase


class TestCrossrefDOIModel(BaseTestCase):
    model_class_to_delete = [CrossrefDOI, Journal]

    def _make_journal(self):
        _id = self.generate_uuid_32_string()
        jid = self.generate_uuid_32_string()
        journal = Journal(**{
            '_id': _id,
            'jid': jid,
            'title': 'The Dummy Journal',
            'acronym': 'dj',
            'is_public': True,
        })
        journal.save()
        return journal

    def test_create_crossrefdoi_required_fields_success(self):
        # given
        journal = self._make_journal()
        crossref_data = {
            'doi': '10.1590/crossmark-policy',
            'is_doi_active': True,
            'language': 'en',
            'journal': journal,
        }

        # when
        crossref_doc = CrossrefDOI(**crossref_data)
        crossref_doc.save()

        # then
        self.assertEqual('10.1590/crossmark-policy', crossref_doc.doi)
        self.assertTrue(crossref_doc.is_doi_active)
        self.assertEqual('en', crossref_doc.language)
        self.assertEqual(journal, crossref_doc.journal)
        self.assertEqual(1, CrossrefDOI.objects.all().count())

    def test_create_crossrefdoi_is_doi_active_default_true(self):
        # given
        journal = self._make_journal()
        crossref_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'pt',
            'journal': journal,
        }

        # when
        crossref_doc = CrossrefDOI(**crossref_data)
        crossref_doc.save()

        # then
        self.assertTrue(crossref_doc.is_doi_active)

    def test_create_crossrefdoi_is_doi_active_false(self):
        # given
        journal = self._make_journal()
        crossref_data = {
            'doi': '10.1590/crossmark-policy',
            'is_doi_active': False,
            'language': 'es',
            'journal': journal,
        }

        # when
        crossref_doc = CrossrefDOI(**crossref_data)
        crossref_doc.save()

        # then
        self.assertFalse(crossref_doc.is_doi_active)

    def test_crossrefdoi_missing_doi_raises_error(self):
        # given
        journal = self._make_journal()
        crossref_data = {
            'language': 'en',
            'journal': journal,
        }

        # when / then
        crossref_doc = CrossrefDOI(**crossref_data)
        with self.assertRaises(ValidationError):
            crossref_doc.save()

    def test_crossrefdoi_missing_language_raises_error(self):
        # given
        journal = self._make_journal()
        crossref_data = {
            'doi': '10.1590/crossmark-policy',
            'journal': journal,
        }

        # when / then
        crossref_doc = CrossrefDOI(**crossref_data)
        with self.assertRaises(ValidationError):
            crossref_doc.save()

    def test_crossrefdoi_missing_journal_raises_error(self):
        # given
        crossref_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
        }

        # when / then
        crossref_doc = CrossrefDOI(**crossref_data)
        with self.assertRaises(ValidationError):
            crossref_doc.save()

    def test_crossrefdoi_unicode(self):
        # given
        journal = self._make_journal()
        crossref_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
            'journal': journal,
        }

        # when
        crossref_doc = CrossrefDOI(**crossref_data)
        crossref_doc.save()

        # then
        self.assertEqual('10.1590/crossmark-policy', crossref_doc.__unicode__())
