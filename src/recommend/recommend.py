import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sympy.strategies.core import switch

embeddings = np.load("content_combined_embeddings.npy")
content_df = pd.read_csv("content_ids.csv")

liked = [(1396, 'tv'),(209867, 'tv'),(299536, 'tv'),(60574, 'tv'),(1416, 'tv')]
disliked = [(271110, 'film')]

def get_indexes(ids_with_type, df):
    idxs = []
    for content_id, content_type in ids_with_type:
        matched = df[(df['id'] == content_id) & (df['content_type'] == content_type)].index
        if not matched.empty:
            idxs.append(matched[0])
    return idxs

liked_indexes = get_indexes(liked, content_df)
if not liked_indexes:
    raise ValueError("Нет валидных понравившихся элементов среди загруженных")

liked_embeddings = embeddings[liked_indexes]
user_profile = liked_embeddings.mean(axis=0)

disliked_indexes = get_indexes(disliked, content_df)
if disliked_indexes:
    disliked_embeddings = embeddings[disliked_indexes]
    user_profile -= disliked_embeddings.mean(axis=0)

similarities = cosine_similarity([user_profile], embeddings)[0]

seen_ids = set(liked + disliked)
recommendation_candidates = [(i, sim) for i, sim in enumerate(similarities)
                             if (content_df.loc[i, 'id'], content_df.loc[i, 'content_type']) not in seen_ids]

recommendation_candidates.sort(key=lambda x: x[1], reverse=True)
top_n = 10
top_indexes = [i for i, sim in recommendation_candidates[:top_n]]
top_recommendations = content_df.loc[top_indexes]

print("Toп рекомендованные фильмы и сериалы:")
for rank, row in enumerate(top_recommendations.itertuples(), 1):
    print(f"{rank}. ID: {row.id}, Тип: {row.content_type}")
