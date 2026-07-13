import pandas as pd


def parse_number(value):
    """
    Converts:
        12.5M -> 12500000
        320K  -> 320000
        1234  -> 1234
        NaN   -> 0
    """

    if pd.isna(value):
        return 0

    value = str(value).replace(",", "").replace("'", "").strip().upper()

    try:
        if value.endswith("M"):
            return int(float(value[:-1]) * 1_000_000)

        if value.endswith("K"):
            return int(float(value[:-1]) * 1_000)

        return int(float(value))

    except:
        return 0


def get_value(row, columns, default=None):
    """
    Returns the first matching column from a dataframe row.
    """

    for col in columns:
        if col in row and pd.notna(row[col]):
            return row[col]

    return default


def normalize_influencer(row, platform):
    """
    Convert every dataset into ONE common schema.
    """

    username = get_value(
        row,
        [
            "Instagram name",
            "instagram name",
            "Influencer insta name",
            "Tiktoker name",
            "Youtuber",
            "youtuber name",
            "Youtube channel",
            "channel name",
            "Username",
        ],
        "",
    )

    full_name = get_value(
        row,
        [
            "Name",
            "name",
            "Tiktok name",
            "Channel name",
            "influencer name",
        ],
        "",
    )

    category = get_value(
        row,
        [
            "Category",
            "Category_1",
            "Category-1",
            "category",
            "category_1",
        ],
        "",
    )

    followers = parse_number(
        get_value(
            row,
            [
                "Followers",
                "#Followers",
                "Subscribers",
                "Subscribers count",
            ],
            0,
        )
    )

    avg_likes = parse_number(
        get_value(
            row,
            [
                "Likes avg",
                "Likes avg.",
                "Likes (Avg.)",
                "avg likes",
                "Engagement avg\r\n",
                "Eng. (Avg.)",
            ],
            0,
        )
    )

    avg_comments = parse_number(
        get_value(
            row,
            [
                "Comments avg",
                "Comments avg.",
                "Comments (Avg.)",
                "avg comments",
            ],
            0,
        )
    )

    return {
        "username": str(username).strip(),
        "full_name": str(full_name).strip(),
        "platform": platform,
        "category": str(category).strip(),
        "followers": followers,
        "avg_likes": avg_likes,
        "avg_comments": avg_comments,
    }
