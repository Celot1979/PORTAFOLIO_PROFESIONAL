from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base

# Define el modelo BlogPost
class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<BlogPost(title='{self.title}')>"

    def save(self, session):
        session.add(self)
        session.commit()