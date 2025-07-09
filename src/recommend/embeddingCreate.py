import psycopg2
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

conn = psycopg2.connect(
    dbname="GigaFilm",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

def embed_text(text):
    if not text or text.strip() == '':
        return np.zeros(model.get_sentence_embedding_dimension())
    return model.encode(text, convert_to_numpy=True)

query_films = """
    SELECT f.id, f.overview, d.name as director_name
    FROM film f
    LEFT JOIN director d ON f.director_id = d.id 
    WHERE 
    f.vote_count > 100
"""
films_df = pd.read_sql_query(query_films, conn)

query_genres = """
    SELECT fg.film_id, g.name as genre_name
    FROM film_genre fg
    JOIN genre g ON fg.genre_id = g.id
"""
genres_df = pd.read_sql_query(query_genres, conn)

query_actors = """
    SELECT fa.tv_id as film_id, a.name as actor_name
    FROM film_actor fa
    JOIN actor a ON fa.actor_id = a.id
"""
actors_df = pd.read_sql_query(query_actors, conn)

film_to_genres = genres_df.groupby('film_id')['genre_name'].apply(list).to_dict()
film_to_actors = actors_df.groupby('film_id')['actor_name'].apply(list).to_dict()

embeddings = []
film_ids = []

for idx, row in films_df.iterrows():
    film_id = row['id']
    overview = row['overview'] if row['overview'] else ''
    director = row['director_name'] if row['director_name'] else ''

    desc_emb = embed_text(overview)

    genres = film_to_genres.get(film_id, [])
    genre_embs = np.array([embed_text(g) for g in genres]) if genres else np.zeros_like(desc_emb)
    genre_emb = genre_embs.mean(axis=0) if len(genres) > 0 else np.zeros_like(desc_emb)

    actors = film_to_actors.get(film_id, [])
    actor_embs = np.array([embed_text(a) for a in actors]) if actors else np.zeros_like(desc_emb)
    actor_emb = actor_embs.mean(axis=0) if len(actors) > 0 else np.zeros_like(desc_emb)

    director_emb = embed_text(director)

    final_emb = np.concatenate([desc_emb, genre_emb, actor_emb, director_emb])

    embeddings.append(final_emb)
    film_ids.append(film_id)


    print(f"Обработано фильмов: {idx}")

embeddings = np.array(embeddings)

np.save('film_combined_embeddings.npy', embeddings)
pd.DataFrame({'id': film_ids}).to_csv('film_ids.csv', index=False)

print("Эмбеддинги созданы и сохранены.")