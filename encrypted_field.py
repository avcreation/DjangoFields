# -*- coding: utf-8 -*-
"""
from django.db import models
import base64


class Base64Encryptor(object):
    def encrypt(self, value):
        return base64.encodestring(value)

    def decrypt(self, msg):
        return base64.decodestring(msg)


class MyModel(models.Model):
    ...
    b64_data = EncryptedField(encryptor=Base64Encryptor)
    ...


# Usage
my_obj = MyModel()
my_obj.b64_data = "hello"
print(my_obj.b64_data)  # will output 'hello'
print(my_obj.b64_data_enc)  # will output 'aGVsbG8=\n'
"""
from __future__ import unicode_literals
from south.modelsinspector import add_introspection_rules
from django.db import models


class BaseEnc(object):
    def encrypt(self, value):
        return value

    def decrypt(self, value):
        return value


class EncryptedField(models.TextField):

    description = "A encrypted field"

    def __init__(self, encryptor=BaseEnc, *args, **kwargs):
        self.encryptor = encryptor()
        super(EncryptedField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name + '_enc'
        super(EncryptedField, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        if getattr(obj, self.field_name):
            return self.encryptor.decrypt(getattr(obj, self.field_name))
        return None

    def set_data(self, obj, data):
        if data:
            setattr(obj, self.field_name, self.encryptor.encrypt(data))
        else:
            setattr(obj, self.field_name, None)

add_introspection_rules([], ["^monprojet.fields.EncryptedField"])
