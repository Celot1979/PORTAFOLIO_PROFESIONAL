from peewee import *
from datetime import datetime
from ..database import db

# Define el modelo BlogPost
class BlogPost(Model):
    title = CharField()
    content = TextField()
    image_url = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db

    def __repr__(self):
        return f"<BlogPost(title='{self.title}')>"

    def save(self):
        self.updated_at = datetime.now()
        return super().save()