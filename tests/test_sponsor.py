# coding: utf-8

from opac_schema.v1.models import Sponsor
from base import BaseTestCase


class TestSponsorModel(BaseTestCase):
    model_class_to_delete = [Sponsor]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        sponsor_data = {
            '_id': _id,
            'name': 'foo sponsor',
        }
        # when
        sponsor_doc = Sponsor(**sponsor_data)
        sponsor_doc.save()

        # then
        self.assertEqual(_id, sponsor_doc._id)
        self.assertEqual(1, Sponsor.objects.all().count())
