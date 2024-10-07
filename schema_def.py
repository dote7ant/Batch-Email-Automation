import Mongo
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from marshmallow import Schema, fields, pre_load, post_load


class ExpiryModel:
    def __init__(self, id, category, file_name, expires, expiry_date):
        self.id = id
        self.category = category
        self.file_name = file_name
        self.expires = expires
        self.expiry_date = expiry_date
        
class ExpiryModelSchema(Schema):
    id = fields.UUID()
    category = fields.Str()
    file_name = fields.Str()
    expires = fields.Bool()
    expiry_date = fields.DateTime()

    @post_load
    def make_expiry_model(self, data, **kwargs):
        return ExpiryModel(**data)