# coding: utf-8

from datetime import datetime
from opac_schema.v1.models import News
from base import BaseTestCase


class TestNewsModel(BaseTestCase):
    model_class_to_delete = [News]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        news_data = {
            '_id': _id,
            'url': 'http://blog.scielo.org',
            'image_url': 'http://blog.scielo.org/sample.png',
            'publication_date': datetime.now(),
            'title': 'foo bar',
            'description': 'lorem ipsum dolor sit ahmet',
            'language': 'en',
            'is_public': True
        }
        # when
        news_doc = News(**news_data)
        news_doc.save()

        # then
        news_count = News.objects.all().count()
        self.assertEqual(_id, news_doc._id)
        self.assertEqual(1, news_count)
