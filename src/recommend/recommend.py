import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class ContentRecommender:
    def __init__(self, embeddings_path="./src/recommend/set/content_combined_embeddings.npy",
                 content_csv="./src/recommend/set/content_ids.csv"):
        self.embeddings = np.load(embeddings_path)
        self.content_df = pd.read_csv(content_csv)

    def get_indexes(self, ids_with_type):
        idxs = []
        for content_id, content_type in ids_with_type:
            matched = self.content_df[
                (self.content_df['id'] == content_id) & (self.content_df['content_type'] == content_type)
            ].index
            if not matched.empty:
                idxs.append(matched[0])
        return idxs

    def recommend(self, liked, disliked=None, unrated=None, top_n=10):
        if disliked is None:
            disliked = []

        if unrated is None:
            unrated = []

        liked_indexes = self.get_indexes(liked)
        liked_embeddings = self.embeddings[liked_indexes]
        user_profile = liked_embeddings.mean(axis=0)

        disliked_indexes = self.get_indexes(disliked)
        if disliked_indexes:
            disliked_embeddings = self.embeddings[disliked_indexes]
            user_profile -= disliked_embeddings.mean(axis=0)

        similarities = cosine_similarity([user_profile], self.embeddings)[0]

        seen_ids = set(liked + disliked + unrated)
        recommendation_candidates = [
            (i, sim) for i, sim in enumerate(similarities)
            if (self.content_df.loc[i, 'id'], self.content_df.loc[i, 'content_type']) not in seen_ids
        ]

        recommendation_candidates.sort(key=lambda x: x[1], reverse=True)
        top_indexes = [i for i, sim in recommendation_candidates[:top_n]]
        top_recommendations = self.content_df.loc[top_indexes]

        result = [
            (row.id, row.content_type)
            for row in top_recommendations.itertuples()
        ]
        return result
    
recomender = ContentRecommender()