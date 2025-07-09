import psycopg2
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# Подключение к БД
conn = psycopg2.connect(
    dbname="GigaFilm",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# Модель
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

def embed_text(text):
    if not text or text.strip() == '':
        return np.zeros(model.get_sentence_embedding_dimension())
    return model.encode(text, convert_to_numpy=True)

query_content = """
    SELECT f.id, f.overview, d.name as director_name, 'film' as content_type
    FROM film f
    LEFT JOIN director d ON f.director_id = d.id 
    WHERE f.vote_count > 50
    UNION ALL
    SELECT t.id, t.overview, NULL as director_name, 'tv' as content_type
    FROM tv t
    WHERE t.vote_count > 50
"""

content_df = pd.read_sql_query(query_content, conn)

query_genres = """
    SELECT film_id as content_id, g.name as genre_name, 'film' as content_type
    FROM film_genre fg
    JOIN genre g ON fg.genre_id = g.id
    UNION ALL
    SELECT tv_id as content_id, g.name as genre_name, 'tv' as content_type
    FROM tv_genre tg
    JOIN genre g ON tg.genre_id = g.id
"""
genres_df = pd.read_sql_query(query_genres, conn)

query_actors = """
    SELECT fa.film_id as content_id, a.name as actor_name, 'film' as content_type
    FROM film_actor fa
    JOIN actor a ON fa.actor_id = a.id
    UNION ALL
    SELECT ta.tv_id as content_id, a.name as actor_name, 'tv' as content_type
    FROM tv_actor ta
    JOIN actor a ON ta.actor_id = a.id
"""
actors_df = pd.read_sql_query(query_actors, conn)

genre_map = genres_df.groupby(['content_id', 'content_type'])['genre_name'].apply(list).to_dict()
actor_map = actors_df.groupby(['content_id', 'content_type'])['actor_name'].apply(list).to_dict()

embeddings = []
content_ids = []
content_types = []

for idx, row in content_df.iterrows():
    content_id = row['id']
    content_type = row['content_type']
    overview = row['overview'] if row['overview'] else ''
    director = row['director_name'] if row['director_name'] else ''

    desc_emb = embed_text(overview)

    genres = genre_map.get((content_id, content_type), [])
    genre_embs = np.array([embed_text(g) for g in genres]) if genres else np.zeros_like(desc_emb)
    genre_emb = genre_embs.mean(axis=0) if len(genres) > 0 else np.zeros_like(desc_emb)

    actors = actor_map.get((content_id, content_type), [])
    actor_embs = np.array([embed_text(a) for a in actors]) if actors else np.zeros_like(desc_emb)
    actor_emb = actor_embs.mean(axis=0) if len(actors) > 0 else np.zeros_like(desc_emb)

    director_emb = embed_text(director)

    final_emb = np.concatenate([desc_emb, genre_emb, actor_emb, director_emb])

    embeddings.append(final_emb)
    content_ids.append(content_id)
    content_types.append(content_type)

    if (idx + 1) % 1000 == 0:
        print(f"Обработано: {idx + 1}/{len(content_df)}")

embeddings = np.array(embeddings)
np.save('content_combined_embeddings.npy', embeddings)

pd.DataFrame({'id': content_ids,'content_type': content_types
              }).to_csv('content_ids.csv', index=False)

print("Эмбеддинги фильмов и сериалов успешно сохранены.")
