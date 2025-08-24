"""
Модуль для очистки и нормализации данных
"""

import pandas as pd

def load_data(path):
    """Загрузка данных"""
    return pd.read_csv(path)

def clean_data(df):
    """Очистка данных"""
    # Удаление дубликатов
    df = df.drop_duplicates()

    # Пропуски
    df['author_city'] = df['author_city'].fillna('Не указано')
    df = df.dropna(subset=['post_text'])

    # Типы данных
    df['post_date'] = pd.to_datetime(df['post_date'])
    df['likes'] = df['likes'].astype(int)
    df['shares'] = df['shares'].astype(int)

    # Выбросы
    df = df[df['likes'] < 10000]

    return df

def normalize_data(df):
    """Нормализация: разделение на authors и posts"""
    authors = df[['author_id', 'author_name', 'author_city']].drop_duplicates().reset_index(drop=True)
    posts = df[['post_id', 'author_id', 'post_text', 'likes', 'shares', 'post_date', 'group_id']].copy()
    return authors, posts

# Пример использования
if __name__ == "__main__":
    df = load_data('../data/raw/posts_raw.csv')
    df_clean = clean_data(df)
    authors, posts = normalize_data(df_clean)
    
    authors.to_csv('../data/processed/authors.csv', index=False)
    posts.to_csv('../data/processed/posts.csv', index=False)
    print("Данные успешно обработаны и сохранены!")
