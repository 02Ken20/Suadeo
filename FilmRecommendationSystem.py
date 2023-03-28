import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# FILM SEARCH RECOMMENDATION ################################
pd.set_option('display.max_columns', None)
pd.options.display.width = 0

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices][::-1]
    return results

def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

movies = pd.read_csv("movies.csv")
movies["clean_title"] = movies["title"].apply(clean_title)

vectorizer = TfidfVectorizer(ngram_range=(1,2))

tfidf = vectorizer.fit_transform(movies["clean_title"])

ratings = pd.read_csv("FilmRatings.csv")

def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]

    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .10]

    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_users_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())

    rec_percentages = pd.concat([similar_user_recs, all_users_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]

    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]

    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(6).merge(movies, left_index=True, right_on="movieId")[["title", "genres"]]

def fromFilmTableToText(table, i):
    text = table.iloc[i]['title'] + '\nGenres: ' + table.iloc[i]['genres'] + '\nYear: ' + str(table.iloc[i]['year']) + '\nRating: ' + str(table.iloc[i]['rating'])
    return text

def recommendFilm(FilmName):
    if len(FilmName) > 5:
        results = search(FilmName)
        movie_id = results.iloc[0]["movieId"]
        recommendation_result = find_similar_movies(movie_id)

        recommendation_result['rating'] = 0
        iteratorI = 0
        filmRatings = pd.read_csv('FilmRatings.csv')
        mean_rating = filmRatings.groupby('movieId')['rating'].mean()
        for i in recommendation_result.iloc[0:6]['title']:
            iteratorJ = 0
            for j in movies['title']:
                if (i == j):
                    movieID = movies.iloc[iteratorJ]['movieId']
                    recommendation_result.iloc[iteratorI, recommendation_result.columns.get_loc('rating')] = mean_rating[movieID]
                iteratorJ += 1
            iteratorI += 1

        recommendation_result['year'] = recommendation_result['title'].str.split('(', n=1).str[1].str.split(')', n=1).str[0]
        recommendation_result['title'] = recommendation_result['title'].str.split('(', n=1).str[0].str.strip()
        recommendation_result = pd.concat([recommendation_result[['title', 'genres', 'rating']], recommendation_result['year']], axis=1)
        recommendation_result['rating'] = recommendation_result['rating'].round(2)

        return recommendation_result

# print("Type the name of a movie: ", end="")
# movie_name_input = input()
# movie_name_input = "Iron Man"
# recommendation_result = recommendFilm(movie_name_input)
# print(recommendation_result)
# print(fromFilmTableToText(recommendation_result, 0))

# year_data = pd.DataFrame({'year': recommendation_result['title'].str.extract(r'\((\d{4})\)', expand=False)})
# recommendation_result['title'] = recommendation_result['title'].str.replace(r'\s*\(\d{4}\)', '')
# recommendation_result = pd.concat([recommendation_result, year_data], axis=1)