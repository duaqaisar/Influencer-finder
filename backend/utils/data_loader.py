import pandas as pd
from glob import glob
from sqlalchemy.orm import Session
from models.post import Post

def load_kaggle_data(db: Session):
    raw_dir = "data/raw"
    csv_files = glob(f"{raw_dir}/*.csv")
    
    print(f"Found {len(csv_files)} CSV files")
    
    all_data = []
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            print(f"Loaded {file} - Shape: {df.shape}")
            all_data.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    if not all_data:
        print("No data loaded")
        return
    
    combined = pd.concat(all_data, ignore_index=True)
    print(f"Combined data shape: {combined.shape}")
    
    # Print column names to see structure
    print("Columns:", combined.columns.tolist())
    
    # Flexible column mapping
    combined = combined.rename(columns={
        'Username': 'username',
        'username': 'username',
        'name': 'username',
        'Platform': 'platform',
        'platform': 'platform',
        'Followers': 'followers',
        'followers': 'followers',
        'Likes': 'likes',
        'Comments': 'comments'
    }, errors='ignore')
    
    # Basic cleaning
    if 'username' in combined.columns:
        combined = combined.dropna(subset=['username'])
        print(f"After cleaning: {len(combined)} rows")
    else:
        print("No username column found")
        return
    
    # Load sample data (limit to avoid too much data for now)
    for _, row in combined.head(5000).iterrows():   # Limit for testing
        try:
            username = str(row.get('username', ''))
            if not username or username == 'nan':
                continue
                
            post = Post(
                platform=str(row.get('platform', 'instagram')).lower(),
                username=username,
                post_text="Sample post from Kaggle dataset",
                likes=int(row.get('likes', 0) or 0),
                comments=int(row.get('comments', 0) or 0),
                shares=0,
                followers=int(row.get('followers', 0) or 0)
            )
            db.add(post)
        except:
            continue
    
    db.commit()
    print(f"Successfully loaded {5000} sample records into database!")
