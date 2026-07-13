import pandas as pd


class ExplanationEngine:

    @staticmethod
    def confidence_score(row: pd.Series):

        score = 40

        if row["posts"] > 0:
            score += 20

        if row["eng_avg"] > 0:
            score += 20

        if row["relevance_score"] > 0.30:
            score += 10

        if row["relevance_score"] > 0.60:
            score += 10

        return min(score, 100)

    @staticmethod
    def selection_reason(row: pd.Series, topic: str):

        reasons = []

        if row["relevance_score"] >= 0.80:
            reasons.append(f"highly relevant to '{topic}'")

        elif row["relevance_score"] >= 0.50:
            reasons.append(f"moderately relevant to '{topic}'")

        else:
            reasons.append(f"loosely related to '{topic}'")

        followers = row["followers"]

        if followers >= 1_000_000:
            reasons.append(
                f"mega influencer with {followers/1_000_000:.1f}M followers"
            )

        elif followers >= 100_000:
            reasons.append(
                f"macro influencer with {followers/1000:.0f}K followers"
            )

        elif followers >= 10_000:
            reasons.append(
                f"micro influencer with {followers/1000:.0f}K followers"
            )

        if row["eng_avg"] > 0 and row["followers"] > 0:

            engagement = (
                row["eng_avg"]
                /
                row["followers"]
            ) * 100

            reasons.append(
                f"engagement rate {engagement:.1f}%"
            )

        if row["posts"] > 0:

            reasons.append(
                f"{int(row['posts'])} posts analyzed"
            )

        return (
            f"@{row['username']} was selected because they are "
            + ", ".join(reasons)
            + "."
        )
