# coding: utf-8

from datetime import datetime
from opac_schema.v1.models import PressRelease
from base import BaseTestCase


class TestPressReleaseModel(BaseTestCase):
    model_class_to_delete = [PressRelease]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        press_release_data = {
            '_id': _id,
            'title': 'foo bar',
            'language': 'en',
            'content': 'lorem ipsum dolor sit ahmet',
            'url': 'http://blog.scielo.org',
            'publication_date': datetime.now(),
        }
        # when
        pr_doc = PressRelease(**press_release_data)
        pr_doc.save()

        # then
        pr_count = PressRelease.objects.all().count()
        self.assertEqual(_id, pr_doc._id)
        self.assertEqual(1, pr_count)
