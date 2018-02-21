# coding: utf-8
from opac_schema.v1.models import Collection
from .base import BaseTestCase


class TestCollectionModels(BaseTestCase):
    model_class_to_delete = [Collection]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        collection_data = {
            '_id': _id,
            'name': 'Dummy Collection',
            'acronym': 'dummy',
        }
        # when
        collection_doc = Collection(**collection_data)
        collection_doc.save()

        # then
        self.assertEqual(_id, collection_doc._id)
        self.assertEqual(1, Collection.objects.all().count())
