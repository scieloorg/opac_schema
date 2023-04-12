# coding: utf-8
from opac_schema.v1.models import Issue
from .base import BaseTestCase
from datetime import datetime


class TestIssueModel(BaseTestCase):
    model_class_to_delete = [Issue]

    def test_create_only_required_fields_success_and_year(self):
        # given
        _id = self.generate_uuid_32_string()
        iid = self.generate_uuid_32_string()
        issue_data = {
            '_id': _id,
            'iid': iid,
            'is_public': True,
            'year': datetime.today().year,  # Year or Volume or Number or Supplement must exists to form URL Issue Segment
        }

        # when
        issue_doc = Issue(**issue_data)
        issue_doc.save()

        # then
        self.assertEqual(_id, issue_doc._id)
        self.assertEqual(iid, issue_doc.iid)
        self.assertEqual(1, Issue.objects.all().count())

    def test_create_only_required_fields_success_and_volume(self):
        # given
        _id = self.generate_uuid_32_string()
        iid = self.generate_uuid_32_string()
        issue_data = {
            '_id': _id,
            'iid': iid,
            'is_public': True,
            'volume': '123'
        }

        # when
        issue_doc = Issue(**issue_data)
        issue_doc.save()

        # then
        self.assertEqual(_id, issue_doc._id)
        self.assertEqual(iid, issue_doc.iid)
        self.assertEqual(1, Issue.objects.all().count())

    def test_create_issue_without_year_volume_and_number(self):
        # given
        _id = self.generate_uuid_32_string()
        iid = self.generate_uuid_32_string()
        issue_data = {
            '_id': _id,
            'iid': iid,
            'is_public': True
        }

        # when
        issue_doc = Issue(**issue_data)

        with self.assertRaises(ValueError) as save_model_exc:
            issue_doc.save()

        # then
        the_exception = save_model_exc.exception
        expected_error_msg = u'Year or Volume or Number or Supplement must exist to form URL Issue Segment'
        self.assertEqual(expected_error_msg, str(the_exception))
        self.assertEqual(0, Issue.objects.all().count())
