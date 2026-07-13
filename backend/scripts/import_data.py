from glob import glob
import os

import pandas as pd
from sqlalchemy.exc import IntegrityError

from core.database import SessionLocal
from models.influencer import Influencer
from services.data_normalizer import normalize_influencer


def detect_platform(filename):
    """
    Detect platform from filename.
    """
    filename = filename.lower()

    if "instagram" in filename:
        return "Instagram"

    if "tiktok" in filename:
        return "TikTok"

    if "youtube" in filename:
        return "YouTube"

    return "Unknown"


def load_dataframe(file_path):
    """
    Load CSV files.
    Skip TXT for now.
    """

    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)

    return None


def main():

    db = SessionLocal()

    files = glob("data/raw/*")

    imported = 0
    skipped = 0
    errors = 0

    print(f"\nFound {len(files)} files.\n")

    for file in files:

        if not file.endswith(".csv"):
            print(f"Skipping {os.path.basename(file)}")
            continue

        print(f"\nProcessing: {os.path.basename(file)}")

        try:

            df = load_dataframe(file)

            if df is None:
                continue

            platform = detect_platform(file)

            for _, row in df.iterrows():

                data = normalize_influencer(row, platform)

                if not data["username"]:
                    skipped += 1
                    continue

                existing = (
                    db.query(Influencer)
                    .filter_by(
                        username=data["username"],
                        platform=platform,
                    )
                    .first()
                )

                if existing:
                    skipped += 1
                    continue

                influencer = Influencer(
                    username=data["username"],
                    full_name=data["full_name"],
                    platform=data["platform"],
                    category=data["category"],
                    followers=data["followers"],
                    avg_likes=data["avg_likes"],
                    avg_comments=data["avg_comments"],
                )

                db.add(influencer)

                try:
                    db.commit()
                    imported += 1

                except IntegrityError:
                    db.rollback()
                    skipped += 1

        except Exception as e:

            print(f"Error processing {file}")
            print(e)

            errors += 1

    db.close()

    print("\n==============================")
    print("IMPORT COMPLETE")
    print("==============================")
    print(f"Imported : {imported}")
    print(f"Skipped  : {skipped}")
    print(f"Errors   : {errors}")


if __name__ == "__main__":
    main()
