from sqlalchemy.orm import Session
from models.influencer import Influencer


class InfluencerRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Influencer).all()

    @staticmethod
    def get_by_platform(db: Session, platform: str):
        return (
            db.query(Influencer)
            .filter(Influencer.platform.ilike(platform))
            .all()
        )

    @staticmethod
    def get_dataframe(db: Session, platform=None):
        """
        Return influencers as a pandas-friendly list of dictionaries.
        """

        if platform:
            influencers = (
                db.query(Influencer)
                .filter(Influencer.platform.ilike(platform))
                .all()
            )
        else:
            influencers = db.query(Influencer).all()

        rows = []

        for influencer in influencers:

            rows.append({
                "username": influencer.username,
                "followers": influencer.followers,
                "posts": influencer.posts_count,
                "eng_avg": influencer.avg_likes + influencer.avg_comments,
                "text": " ".join(filter(None, [
                    influencer.category,
                    influencer.bio,
                    influencer.full_name
                ])),
                "platform": influencer.platform,
            })

        return rows
