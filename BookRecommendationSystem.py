import numpy as np  # linear algebra
import re
import csv
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option('display.max_columns', None)
pd.options.display.width = 0

books = pd.read_csv('books.csv', encoding = "ISO-8859-1")
ratings = pd.read_csv('ratings.csv', encoding = "ISO-8859-1")
book_tags = pd.read_csv('book_tags.csv', encoding = "ISO-8859-1")
tags = pd.read_csv('tags.csv')
tags_join_DF = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')
to_read = pd.read_csv('to_read.csv')
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(books['authors'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

titles = books['title']
indices = pd.Series(books.index, index=books['title'])

def clean_title(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)
books["title"] = books["title"].apply(clean_title)
default_value = -1
books['original_publication_year'] = books['original_publication_year'].fillna(default_value)
books['original_publication_year'] = np.where(np.isinf(books['original_publication_year']), default_value, books['original_publication_year'])
books["original_publication_year"] = books["original_publication_year"].astype(int)

vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf = vectorizer.fit_transform(books["title"])
def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = books.iloc[indices][::-1]
    return results.iloc[0]['title']

# Function that get book recommendations based on the cosine similarity score of book authors
def authors_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]

books_with_tags = pd.merge(books, tags_join_DF, left_on='book_id', right_on='goodreads_book_id', how='inner')
tf1 = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix1 = tf1.fit_transform(books_with_tags['tag_name'].head(10000))
cosine_sim1 = linear_kernel(tfidf_matrix1, tfidf_matrix1)

titles1 = books['title']
indices1 = pd.Series(books.index, index=books['title'])

# Function that get book recommendations based on the cosine similarity score of books tags
def tags_recommendations(title):
    idx = indices1[title]
    sim_scores = list(enumerate(cosine_sim1[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]

temp_df = books_with_tags.groupby('book_id')['tag_name'].apply(' '.join).reset_index()
books = pd.merge(books, temp_df, left_on='book_id', right_on='book_id', how='inner')

books['corpus'] = (pd.Series(books[['authors', 'tag_name']]
                .fillna('')
                .values.tolist()
                ).str.join(' '))

tf_corpus = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix_corpus = tf_corpus.fit_transform(books['corpus'])
cosine_sim_corpus = linear_kernel(tfidf_matrix_corpus, tfidf_matrix_corpus)

# Build a 1-dimensional array with book titles
titles = books[['title', 'authors', 'original_publication_year']]
indices = pd.Series(books.index, index=books['title'])

def fromBookTableToText(table, i):
    text = table.iloc[i]['title'] + '\nAuthors: ' + table.iloc[i]['authors'] + '\nYear: ' + str(table.iloc[i]['original_publication_year']) + '\nRating: ' + str(table.iloc[i]['rating'])
    return text

# Function that get book recommendations based on the cosine similarity score of books tags
def recommendBook(bookName):
    title = search(bookName)
    idx = indices1[title]
    sim_scores = list(enumerate(cosine_sim_corpus[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    result = titles.iloc[book_indices].head(6)
    result = pd.DataFrame(result)
    result['rating'] = 0

    iteratorI = 0
    bookRatings = pd.read_csv('ratings.csv')
    mean_rating = bookRatings.groupby('book_id')['rating'].mean()
    for i in result.iloc[0:6]['title']:
        iteratorJ = 0
        for j in books['title']:
            if (i == j):
                book_id = books.iloc[iteratorJ]['id']
                result.iloc[iteratorI, result.columns.get_loc('rating')] = mean_rating[book_id]
            iteratorJ += 1
        iteratorI += 1
    return result

# print("Type the name of a book: ", end="")
# book_name_input = input()
# recommendation_result = recommendBook(book_name_input)
# print(recommendation_result)
# print(fromBookTableToText(recommendation_result, 0))