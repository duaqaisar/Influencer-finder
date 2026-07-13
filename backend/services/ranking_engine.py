import numpy as np
import pandas as pd


class RankingEngine:


    @staticmethod
    def safe_numeric(series):
        return pd.to_numeric(
            series,
            errors="coerce"
        ).fillna(0)



    @staticmethod
    def log_scale(series):

        values = np.log1p(
            RankingEngine.safe_numeric(series)
            .clip(lower=0)
        )

        max_value = values.max()

        if max_value == 0:
            return values

        return values / max_value



    @classmethod
    def calculate_influence(
        cls,
        df: pd.DataFrame
    ):

        """
        Measures social influence.

        Components:

        40% Followers
        35% Engagement
        25% Activity
        """


        followers = cls.safe_numeric(
            df.get(
                "followers",
                0
            )
        )


        likes = cls.safe_numeric(
            df.get(
                "avg_likes",
                0
            )
        )


        posts = cls.safe_numeric(
            df.get(
                "posts_count",
                0
            )
        )


        follower_score = (
            cls.log_scale(followers)
            * 0.40
        )


        engagement_rate = (
            likes /
            followers.replace(
                0,
                np.nan
            )
        ).fillna(0)


        engagement_score = (
            cls.log_scale(
                engagement_rate
            )
            *
            0.35
        )


        activity_score = (
            cls.log_scale(posts)
            *
            0.25
        )


        return (
            follower_score
            +
            engagement_score
            +
            activity_score
        ).clip(0,1)



    @staticmethod
    def calculate_expertise(
        df: pd.DataFrame
    ):

        """
        Measures niche expertise.
        """


        keywords = [
            "fitness",
            "gym",
            "workout",
            "training",
            "bodybuilding",
            "exercise",
            "muscle",
            "strength",
            "cardio",
            "nutrition",
            "coach",
            "athlete"
        ]


        scores=[]


        for text in df["text"].astype(str):

            text=text.lower()

            hits=sum(
                1
                for k in keywords
                if k in text
            )

            scores.append(
                min(
                    hits /
                    len(keywords),
                    1
                )
            )


        return pd.Series(
            scores,
            index=df.index
        )



    @staticmethod
    def calculate_authority(
        df: pd.DataFrame
    ):

        """
        Authority score.

        Based on:
        - verification
        - followers
        - expertise
        """


        verified = (
            pd.to_numeric(
                df.get(
                    "verified",
                    0
                ),
                errors="coerce"
            )
            .fillna(0)
            .astype(float)
        )


        followers = pd.to_numeric(
            df.get(
                "followers",
                0
            ),
            errors="coerce"
        ).fillna(0)



        follower_authority = (
            RankingEngine.log_scale(
                followers
            )
        )


        authority = (

            follower_authority * 0.50

            +

            verified * 0.20

            +

            df.get(
                "expertise_score",
                0
            )
            *
            0.30

        )


        return authority.clip(
            0,
            1
        )



    @staticmethod
    def calculate_overall(
        df: pd.DataFrame
    ):

        """
        Final ranking score.

        Relevance is strongest factor.
        """


        relevance = (
            pd.to_numeric(
                df.get(
                    "relevance_score",
                    0
                ),
                errors="coerce"
            )
            .fillna(0)
        )


        influence = (
            pd.to_numeric(
                df.get(
                    "influence_score",
                    0
                ),
                errors="coerce"
            )
            .fillna(0)
        )


        authority = (
            pd.to_numeric(
                df.get(
                    "authority_score",
                    0
                ),
                errors="coerce"
            )
            .fillna(0)
        )



        overall=(

            relevance * 0.50

            +

            influence * 0.25

            +

            authority * 0.25

        )


        return overall.clip(
            0,
            1
        )
