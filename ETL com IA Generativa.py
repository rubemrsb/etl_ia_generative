import pandas as pd
import openai
import time
import os

# EXTRACT DE DADOS

file_path = 'C:/Users/rubem/Desktop/dio-python/ETL IMDB/imdb-movies-dataset.csv'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

df = pd.read_csv(file_path)
movie_names = df['Title'].tolist()

# TRANSFORMAÇÃO COM IA GENERATIVA

openai_api_key = 'Adicionar a sua key'
openai.api_key = openai_api_key


def generate_ai_sinopsis(movie_name):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em filmes."},
                {"role": "user", "content": f"Crie uma sinopse para {
                    movie_name} (máximo de 100 caracteres)"}
            ]
        )
        return response.choices[0].message['content'].strip('\"')
    except Exception as e:
        print(f"Erro ao gerar sinopse para {movie_name}: {e}")
        return "Sinopse não disponível"


sinopses = []

for movie in movie_names:
    sinopsis = generate_ai_sinopsis(movie)
    print(sinopsis)
    sinopses.append(sinopsis)
    # Pausa de 1 segundo entre as chamadas para evitar limite de taxa
    time.sleep(1)

# Adicione a lista de sinopses ao DataFrame
df['Sinopse'] = sinopses

# LOAD
df.to_csv('C:/Users/rubem/Desktop/dio-python/ETL IMDB/imdb-movies-dataset-with-synopsis.csv', index=False)
