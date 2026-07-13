from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)

    full_name = Column(String)

    platform = Column(String)

    bio = Column(Text)

    category = Column(String)

    followers = Column(Integer, default=0)

    following = Column(Integer, default=0)

    posts_count = Column(Integer, default=0)

    avg_likes = Column(Float, default=0)

    avg_comments = Column(Float, default=0)

    engagement_rate = Column(Float, default=0)

    verified = Column(Boolean, default=False)

    profile_url = Column(String)

    relevance_score = Column(Float, default=0)

    influence_score = Column(Float, default=0)

    overall_score = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship(
        "Post",
        back_populates="influencer",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Influencer {self.username}>"
