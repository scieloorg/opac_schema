# coding: utf-8
from datetime import datetime
from mongoengine import ValidationError
from .base import BaseTestCase
from opac_schema.v1.models import AuditLogEntry


class AuditLogEntryModel(BaseTestCase):
    model_class_to_delete = [AuditLogEntry]

    def test_create_only_required_fields_success(self):
        # given
        _id = self.generate_uuid_32_string()
        entry_data = {
            '_id': _id,
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()

        # then
        self.assertEqual(_id, entry_doc._id)
        self.assertEqual(1, AuditLogEntry.objects.all().count())

    def test_created_at_is_filled_properly(self):
        # given
        entry_data = {
            '_id': self.generate_uuid_32_string(),
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()

        # then
        self.assertIsNotNone(entry_doc.created_at)

    def test_create_entry_with_add_action(self):
        # given
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'action': 'ADD'
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()

        # then
        self.assertEqual("ADD", entry_doc.action)
        self.assertEqual("Add", entry_doc.get_action_value)

    def test_create_entry_with_update_action(self):
        # given
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'action': 'UPD'
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()

        # then
        self.assertEqual("UPD", entry_doc.action)
        self.assertEqual("Update", entry_doc.get_action_value)

    def test_create_entry_with_delete_action(self):
        # given
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'action': 'DEL'
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()

        # then
        self.assertEqual("DEL", entry_doc.action)
        self.assertEqual("Delete", entry_doc.get_action_value)

    def test_create_entry_with_invalid_action_raise_error(self):
        # given
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'action': 'FOO'
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)

        # then
        with self.assertRaises(ValidationError) as save_model_exc:
            entry_doc.save()

        the_exception = save_model_exc.exception
        # check error message in two parts because it's different in py2 and py3
        # py2: Value must be one of ['ADD', 'DEL', 'UPD']: ['action']
        # py3: Value must be one of dict_keys(['ADD', 'UPD', 'DEL']): ['action'])
        # py3 has an extra word: "dict_keys(...)"
        expected_error_msg_part_1 = "Value must be one of "
        self.assertIn(expected_error_msg_part_1, str(the_exception))
        expected_error_msg_part_2 = "['ADD', 'DEL', 'UPD']"
        self.assertIn(expected_error_msg_part_2, str(the_exception))
        self.assertEqual(0, AuditLogEntry.objects.all().count())

    def test_create_entry_with_an_email_as_user_info(self):
        # given
        user_info = 'juan.funez@example.com'
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'user': user_info
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()
        # then
        self.assertEqual(user_info, entry_doc.user)

    def test_create_entry_with_uuid32_string_as_user_info(self):
        # given
        user_info = self.generate_uuid_32_string()
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'user': user_info
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()
        # then
        self.assertEqual(user_info, entry_doc.user)

    def test_create_entry_with_uuid32_string_as_object_pk(self):
        # given
        object_pk = self.generate_uuid_32_string()
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'object_pk': object_pk
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()
        # then
        self.assertEqual(object_pk, entry_doc.object_pk)

    def test_create_entry_with_too_large_string_as_object_pk_raise_error(self):
        # given
        object_pk = self.generate_uuid_32_string() + 'x'
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'object_pk': object_pk
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        with self.assertRaises(ValidationError) as save_model_exc:
            entry_doc.save()

        # then
        the_exception = save_model_exc.exception
        expected_error_msg = "String value is too long: ['object_pk']"
        self.assertIn(expected_error_msg, str(the_exception))
        self.assertEqual(0, AuditLogEntry.objects.all().count())

    def test_create_entry_with_random_fields_data_success(self):
        # given
        fields_data = {
            'str_val': 'foo value',
            'integer_val': 99999,
            'float_val': float('0.9999'),
            'date_val': datetime.today(),
            'date_time_val': datetime.now(),
        }
        entry_data = {
            '_id': self.generate_uuid_32_string(),
            'fields_data': fields_data
        }
        # when
        entry_doc = AuditLogEntry(**entry_data)
        entry_doc.save()
        # then
        self.assertEqual(fields_data, entry_doc.fields_data)
