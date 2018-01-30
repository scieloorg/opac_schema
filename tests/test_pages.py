# coding: utf-8
from time import sleep
from opac_schema.v1.models import Pages
from base import BaseTestCase


class TestPagesModel(BaseTestCase):
    model_class_to_delete = [Pages]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        page_data = {
            '_id': _id,
            'name': 'foo',
            'language': 'en',
            'content': 'lorem ipsum',
        }

        # when
        page_doc = Pages(**page_data)
        page_doc.save()

        # then
        pages_count = Pages.objects.all().count()
        self.assertEqual(1, pages_count)
        self.assertEqual(_id, page_doc._id)

    def test_check_upated_at_is_updated(self):
        # given
        _id = self.generate_uuid_32_string()
        page_data = {
            '_id': _id,
            'name': 'foo',
            'language': 'en',
            'content': 'lorem ipsum',
        }

        # when
        page_doc = Pages(**page_data)
        page_doc.save()
        initial_updated_at = page_doc.updated_at
        sleep(1)
        page_doc.save()
        final_updated_at = page_doc.updated_at

        # then
        self.assertTrue(initial_updated_at < final_updated_at)
