import pandas as pd


from services.influencer_profile_builder import (
    InfluencerProfileBuilder
)

from services.embedding_cache import (
    EmbeddingCache
)

from services.relevance_engine import (
    RelevanceEngine
)

from services.ranking_engine import (
    RankingEngine
)

from services.explanation_engine import (
    ExplanationEngine
)



class InfluencerService:



    def find_influencers(
        self,
        topic: str,
        top_n: int = 10,
        platform: str = None
    ):


        profiles = (
            InfluencerProfileBuilder
            .build_profiles()
        )



        if not profiles:

            return {
                "message":
                "No influencers found."
            }



        df = pd.DataFrame(
            profiles
        )



        # platform filtering

        if platform:

            df = df[
                df["platform"]
                .str.lower()
                ==
                platform.lower()
            ]



        if df.empty:

            return {
                "message":
                "No influencers found."
            }



        # cleaning

        df = df.fillna("")

        df = df[
            df["username"]
            .astype(str)
            .str.len()
            > 1
        ]



        df = (
            df
            .drop_duplicates(
                subset=[
                    "username"
                ]
            )
            .reset_index(
                drop=True
            )
        )



        # relevance

        relevance, keywords = (
            RelevanceEngine
            .hybrid_relevance(
                df["text"],
                topic
            )
        )


        df["relevance_score"] = (
            relevance
        )



        # influence

        df["influence_score"] = (
            RankingEngine
            .calculate_influence(df)
        )



        # authority

        df["authority_score"] = (
            RankingEngine
            .calculate_authority(
                df,
                topic
            )
        )



        # final score

        df["overall_score"] = (
            RankingEngine
            .calculate_overall(df)
        )



        # confidence

        df["confidence_score"] = (
            df.apply(
                ExplanationEngine
                .confidence_score,
                axis=1
            )
        )



        # explanation

        df["selection_reason"] = (
            df.apply(
                lambda row:
                ExplanationEngine
                .selection_reason(
                    row,
                    topic
                ),
                axis=1
            )
        )



        # ranking

        df = (
            df
            .sort_values(
                "overall_score",
                ascending=False
            )
            .head(top_n)
            .reset_index(
                drop=True
            )
        )



        results=[]



        for idx,row in df.iterrows():


            results.append({

                "rank":
                    idx + 1,


                "username":
                    row["username"],


                "category":
                    row.get(
                        "category",
                        ""
                    ),


                "followers":
                    int(
                        row.get(
                            "followers",
                            0
                        )
                    ),


                "relevance_score":
                    round(
                        float(
                            row["relevance_score"]
                        ),
                        4
                    ),


                "influence_score":
                    round(
                        float(
                            row["influence_score"]
                        ),
                        4
                    ),


                "authority_score":
                    round(
                        float(
                            row["authority_score"]
                        ),
                        4
                    ),


                "overall_score":
                    round(
                        float(
                            row["overall_score"]
                        ),
                        4
                    ),


                "confidence_score":
                    round(
                        float(
                            row["confidence_score"]
                        ),
                        1
                    ),


                "selection_reason":
                    row[
                        "selection_reason"
                    ],


                "keywords":
                    keywords[:5]

            })



        return results
