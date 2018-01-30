# coding: utf-8
from opac_schema.v1.models import Journal
from base import BaseTestCase


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
            'is_public': True
        }

        # when
        journal_doc = Journal(**journal_data)
        journal_doc.save()

        # then
        self.assertEqual(_id, journal_doc._id)
        self.assertEqual(jid, journal_doc.jid)
        self.assertEqual(1, Journal.objects.all().count())
