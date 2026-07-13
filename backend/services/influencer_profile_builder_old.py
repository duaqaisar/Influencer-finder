from sqlalchemy import text

from core.database import SessionLocal


class InfluencerProfileBuilder:


    @staticmethod
    def clean(value):

        if value is None:
            return ""

        return str(value)



    @staticmethod
    def build_profiles():

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

                    COUNT(p.id) AS posts,

                    AVG(
                        COALESCE(p.likes,0)
                        +
                        COALESCE(p.comments,0)
                    ) AS eng_avg,


                    GROUP_CONCAT(
                        p.caption,
                        ' '
                    ) AS captions,


                    GROUP_CONCAT(
                        p.hashtags,
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


                username = InfluencerProfileBuilder.clean(
                    row.username
                )


                platform = InfluencerProfileBuilder.clean(
                    row.platform
                )


                category = InfluencerProfileBuilder.clean(
                    row.category
                )


                bio = InfluencerProfileBuilder.clean(
                    row.bio
                )


                captions = InfluencerProfileBuilder.clean(
                    row.captions
                )


                hashtags = InfluencerProfileBuilder.clean(
                    row.hashtags
                )


                profile_text = " ".join(
                    [
                        username,
                        platform,
                        category,
                        bio,
                        captions,
                        hashtags,
                    ]
                )



                profiles.append({

                    "id": row.id,

                    "username": username,

                    "platform": platform,

                    "category": category,

                    "bio": bio,


                    "followers":
                        int(row.followers or 0),


                    "following":
                        int(row.following or 0),


                    "posts_count":
                        int(row.posts_count or 0),


                    # compatibility with old code
                    "posts":
                        int(row.posts or 0),


                    "avg_likes":
                        float(row.avg_likes or 0),


                    "avg_comments":
                        float(row.avg_comments or 0),


                    "eng_avg":
                        float(row.eng_avg or 0),


                    "engagement_rate":
                        float(
                            row.engagement_rate or 0
                        ),


                    "verified":
                        bool(row.verified),



                    "text":
                        profile_text.strip()

                })


            print(
                f"[ProfileBuilder] Built {len(profiles)} profiles"
            )


            return profiles



        finally:

            db.close()

