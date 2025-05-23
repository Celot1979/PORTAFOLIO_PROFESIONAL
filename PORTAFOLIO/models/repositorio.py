from peewee import *
from ..database import db

class Repositorio(Model):
    titulo = CharField()
    enlace = CharField()
    imagen = CharField()

    class Meta:
        database = db

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs).save()

    @classmethod
    def delete_by_id(cls, id):
        cls.delete().where(cls.id == id).execute() 