from core.database import Base, engine

from models.influencer import Influencer
from models.post import Post

Base.metadata.create_all(bind=engine)

print("Database created successfully!")
