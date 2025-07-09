import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

embeddings = np.load("./set/film_combined_embeddings.npy")

film_ids = pd.read_csv("film_ids.csv")["id"].tolist()

liked_ids = [299536,157336,293660,671,106646,11324,150540,451048,507086]   
disliked_ids = [254,591634,447061,672]     

liked_indexes = [i for i, fid in enumerate(film_ids) if fid in liked_ids]
if not liked_indexes:
    raise ValueError("Нет валидных ID понравившихся фильмов среди загруженных")

liked_embeddings = embeddings[liked_indexes]
user_profile = liked_embeddings.mean(axis=0)

disliked_indexes = [i for i, fid in enumerate(film_ids) if fid in disliked_ids]
if disliked_indexes:
    disliked_embeddings = embeddings[disliked_indexes]
    user_profile -= disliked_embeddings.mean(axis=0)

similarities = cosine_similarity([user_profile], embeddings)[0]

seen_ids = set(liked_ids + disliked_ids)
recommendation_candidates = [(i, sim) for i, sim in enumerate(similarities) if film_ids[i] not in seen_ids]

recommendation_candidates.sort(key=lambda x: x[1], reverse=True)
top_n = 10
top_indexes = [i for i, sim in recommendation_candidates[:top_n]]
top_ids = [film_ids[i] for i in top_indexes]

print("Top рекомендованные фильмы (по ID):")
for rank, fid in enumerate(top_ids, 1):
    print(f"{rank}. ID: https://www.themoviedb.org/movie/{fid}")