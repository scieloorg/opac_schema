# coding: utf-8
import time
from mongoengine import ValidationError
from opac_schema.v1.models import CrossmarkPage, Journal
from .base import BaseTestCase


class TestCrossmarkPageModel(BaseTestCase):
    model_class_to_delete = [CrossmarkPage, Journal]

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

    def test_create_crossmarkpage_required_fields_success(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'is_doi_active': True,
            'language': 'en',
            'journal': journal,
        }

        # when
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()

        # then
        self.assertEqual('10.1590/crossmark-policy', crossmark_doc.doi)
        self.assertTrue(crossmark_doc.is_doi_active)
        self.assertEqual('en', crossmark_doc.language)
        self.assertEqual(journal, crossmark_doc.journal)
        self.assertEqual(1, CrossmarkPage.objects.all().count())

    def test_create_crossmarkpage_is_doi_active_default_true(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'pt',
            'journal': journal,
        }

        # when
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()

        # then
        self.assertTrue(crossmark_doc.is_doi_active)

    def test_create_crossmarkpage_is_doi_active_false(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'is_doi_active': False,
            'language': 'es',
            'journal': journal,
        }

        # when
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()

        # then
        self.assertFalse(crossmark_doc.is_doi_active)

    def test_crossmarkpage_missing_doi_raises_error(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'language': 'en',
            'journal': journal,
        }

        # when / then
        crossmark_doc = CrossmarkPage(**crossmark_data)
        with self.assertRaises(ValidationError):
            crossmark_doc.save()

    def test_crossmarkpage_missing_language_raises_error(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'journal': journal,
        }

        # when / then
        crossmark_doc = CrossmarkPage(**crossmark_data)
        with self.assertRaises(ValidationError):
            crossmark_doc.save()

    def test_crossmarkpage_missing_journal_raises_error(self):
        # given
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
        }

        # when / then
        crossmark_doc = CrossmarkPage(**crossmark_data)
        with self.assertRaises(ValidationError):
            crossmark_doc.save()

    def test_crossmarkpage_unicode(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
            'journal': journal,
        }

        # when
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()

        # then
        self.assertEqual('10.1590/crossmark-policy', crossmark_doc.__unicode__())

    def test_crossmarkpage_created_at_set_on_save(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
            'journal': journal,
        }

        # when
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()

        # then
        self.assertIsNotNone(crossmark_doc.created_at)

    def test_crossmarkpage_updated_at_set_on_save(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
            'journal': journal,
        }

        # when
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()

        # then
        self.assertIsNotNone(crossmark_doc.updated_at)

    def test_crossmarkpage_created_at_unchanged_on_update(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
            'journal': journal,
        }
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()
        created_at_first = crossmark_doc.created_at

        # when
        crossmark_doc.doi = '10.1590/crossmark-policy-updated'
        crossmark_doc.save()

        # then
        self.assertEqual(created_at_first, crossmark_doc.created_at)

    def test_crossmarkpage_updated_at_changes_on_update(self):
        # given
        journal = self._make_journal()
        crossmark_data = {
            'doi': '10.1590/crossmark-policy',
            'language': 'en',
            'journal': journal,
        }
        crossmark_doc = CrossmarkPage(**crossmark_data)
        crossmark_doc.save()
        updated_at_first = crossmark_doc.updated_at

        # when
        time.sleep(0.01)
        crossmark_doc.doi = '10.1590/crossmark-policy-updated'
        crossmark_doc.save()

        # then
        self.assertGreater(crossmark_doc.updated_at, updated_at_first)
