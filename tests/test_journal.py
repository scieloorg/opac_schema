# coding: utf-8
from six import string_types
from opac_schema.v1.models import Journal
from .base import BaseTestCase


class TestJournalModel(BaseTestCase):
    model_class_to_delete = [Journal]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        jid = self.generate_uuid_32_string()
        journal_data = {
            '_id': _id,
            'jid': jid,
            'title': 'The Dummy Journal',
            'acronym': 'dj',
            'is_public': True,
            'scimago_id': '4500151524',
        }

        # when
        journal_doc = Journal(**journal_data)
        journal_doc.save()

        # then
        self.assertEqual('4500151524', journal_doc.scimago_id)
        self.assertEqual(_id, journal_doc._id)
        self.assertEqual(jid, journal_doc.jid)
        self.assertEqual(1, Journal.objects.all().count())

    def test_if_editor_email_field_accept_text(self):
        _id = self.generate_uuid_32_string()
        jid = self.generate_uuid_32_string()
        journal_data = {
            '_id': _id,
            'jid': jid,
            'title': 'The Dummy Journal Editor_email',
            'acronym': 'dj',
            'is_public': True,
            'scimago_id': '4500151524',
            'editor_email': 'example1@emial.com;example2@emial.com;'
        }

        journal_doc = Journal(**journal_data)
        journal_doc.save()

        self.assertTrue(isinstance(journal_doc.editor_email, string_types))
