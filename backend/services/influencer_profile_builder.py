from sqlalchemy import text

from core.database import SessionLocal


class InfluencerProfileBuilder:

    @staticmethod
    def clean(value):
        if value is None:
            return ""
        return value

    @classmethod
    def build_profiles(cls):

        db = SessionLocal()

        try:

            query = text("""
                SELECT
                    i.id,
                    i.username,
                    i.full_name,
                    i.platform,
                    i.bio,
                    i.category,
                    i.followers,
                    i.following,
                    i.posts_count,
                    i.avg_likes,
                    i.avg_comments,
                    i.engagement_rate,
                    i.verified,

                    GROUP_CONCAT(
                        COALESCE(p.caption,''),
                        ' '
                    ) AS captions,

                    GROUP_CONCAT(
                        COALESCE(p.hashtags,''),
                        ' '
                    ) AS hashtags

                FROM influencers i

                LEFT JOIN posts p
                    ON i.id = p.influencer_id

                GROUP BY i.id
            """)

            rows = db.execute(query).fetchall()

            profiles = []

            for row in rows:

                username = cls.clean(row.username)
                fullname = cls.clean(row.full_name)
                platform = cls.clean(row.platform)
                category = cls.clean(row.category)
                bio = cls.clean(row.bio)
                captions = cls.clean(row.captions)
                hashtags = cls.clean(row.hashtags)

                profile_text = " ".join([
                    str(fullname),
                    str(username),
                    str(platform),
                    str(category),
                    str(bio),
                    str(captions),
                    str(hashtags)
                ])

                profiles.append({

                    "id": row.id,

                    "username": username,

                    "full_name": fullname,

                    "platform": platform,

                    "category": category,

                    "bio": bio,

                    "followers": row.followers or 0,

                    "following": row.following or 0,

                    "posts_count": row.posts_count or 0,

                    "avg_likes": row.avg_likes or 0,

                    "avg_comments": row.avg_comments or 0,

                    "engagement_rate": row.engagement_rate or 0,

                    "verified": bool(row.verified),

                    "text": profile_text.strip()

                })

            print(f"[ProfileBuilder] Built {len(profiles)} profiles")

            return profiles

        finally:

            db.close()