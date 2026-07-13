from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    influencer_id = Column(
        Integer,
        ForeignKey("influencers.id"),
        nullable=False,
    )

    platform = Column(String, index=True)

    caption = Column(Text)

    hashtags = Column(JSON)

    likes = Column(Integer, default=0)

    comments = Column(Integer, default=0)

    shares = Column(Integer, default=0)

    views = Column(Integer, default=0)

    timestamp = Column(DateTime, default=datetime.utcnow)

    post_url = Column(String, nullable=True)

    influencer = relationship(
        "Influencer",
        back_populates="posts",
    )

    def __repr__(self):
        return f"<Post {self.id}>"
