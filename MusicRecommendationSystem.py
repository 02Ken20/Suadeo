import numpy as np
import pandas as pd
import numpy as np


from sklearn.preprocessing import OrdinalEncoder
from sklearn.cluster import KMeans

from scipy import stats
from sklearn.preprocessing import StandardScaler

from sklearn.metrics.pairwise import cosine_similarity

pd.options.mode.chained_assignment = None  # default='warn'

pd.set_option('display.max_columns', None)
pd.options.display.width = 0

data = pd.read_csv("SpotifyFeatures.csv")

indx = data[['track_name', 'artist_name']]
attributes = data.drop(['track_id', 'time_signature','track_name', 'artist_name', 'key'], axis = 1)

ordinal_encoder = OrdinalEncoder()
object_cols = ['mode']
attributes[object_cols] = ordinal_encoder.fit_transform(attributes[object_cols])

attributes = pd.get_dummies(attributes)
attributes.insert(loc=0, column='track_name', value=indx.track_name)
attributes.insert(loc=1, column = 'artist_name', value = indx.artist_name)

genres_names = ['genre_A Capella', 'genre_Alternative', 'genre_Anime', 'genre_Blues',
       "genre_Children's Music", "genre_Children’s Music", 'genre_Classical',
       'genre_Comedy', 'genre_Country', 'genre_Dance', 'genre_Electronic',
       'genre_Folk', 'genre_Hip-Hop', 'genre_Indie', 'genre_Jazz',
       'genre_Movie', 'genre_Opera', 'genre_Pop', 'genre_R&B', 'genre_Rap',
       'genre_Reggae', 'genre_Reggaeton', 'genre_Rock', 'genre_Ska',
       'genre_Soul', 'genre_Soundtrack', 'genre_World']

genres = attributes.groupby(['track_name', 'artist_name'])[genres_names].sum()

column_names = ['track_name', 'artist_name']
for i in genres_names:
    column_names.append(i)

genres.reset_index(inplace=True)
genres.columns = column_names

attributes = attributes.drop(genres_names, axis = 1)

atts_cols = attributes.drop(['track_name', 'artist_name'], axis = 1).columns
scaler = StandardScaler()
attributes[atts_cols] = scaler.fit_transform(attributes[atts_cols])

songs = pd.merge(genres, attributes, how = 'inner', on = ['track_name', "artist_name"])
songs = songs.drop_duplicates(['track_name', 'artist_name']).reset_index(drop = True)

DF = pd.DataFrame(songs.drop(['track_name', 'artist_name'], axis = 1))
kmeans = KMeans(n_clusters=17)
songs['Cluster'] = kmeans.fit_predict(DF)


def find_song_database(name, artist, songs):
    result = songs[(songs.artist_name == str(artist)) & (songs.track_name == str(name))]
    if len(result) == 0:
        return None
    return result.drop(['track_name', 'artist_name', 'Cluster'], axis=1)


def find_similar(name, artist, songs, top_n=5):
    database = songs[songs.popularity > 0.5].reset_index(drop=True)
    indx_names = database[['track_name', 'artist_name', 'Cluster']]
    songs_train = database.drop(['track_name', 'artist_name', 'Cluster'], axis=1)

    song = find_song_database(str(name), str(artist), database)

    if type(song) != type(None):


        indx_song = song.index

        cos_dists = cosine_similarity(songs_train, songs_train)
        indx_names.loc[:, ['result']] = cos_dists[indx_song[0]]

        indx_names = indx_names.sort_values(by=['result'], ascending=False)
        indx_names = pd.DataFrame(indx_names)
        indx_names.insert(3,"popularity", " ")
        indx_names.insert(4,"genre", " ")

        temp = [{} for i in range(6)]
        result = pd.DataFrame(data=temp, columns=['track_name', 'artist_name', 'popularity', 'genre'])

        iteratorI = 1
        for i in indx_names.iloc[1:top_n]['track_name']:
            iteratorJ = 0
            for j in data['track_name']:
                if (i == j):
                    result.loc[iteratorI - 1, 'track_name'] = data.iloc[iteratorJ]['track_name']
                    result.loc[iteratorI - 1, 'artist_name'] = data.iloc[iteratorJ]['artist_name']
                    result.loc[iteratorI - 1, 'popularity'] = data.iloc[iteratorJ]['popularity'] / 10
                    result.loc[iteratorI - 1, 'genre'] = data.iloc[iteratorJ]['genre']
                    break
                iteratorJ += 1
            iteratorI += 1

        result.fillna(' ', inplace=True)
        return result

    else:
        print("Song not found")
        return None

def fromMusicTableToText(table, i):
    text = table.iloc[i]['track_name'] + '\nArtist: ' + table.iloc[i]['artist_name'] + '\nPopularity: ' + str(table.iloc[i]['popularity']) + '\nGenre: ' + table.iloc[i]['genre']
    return text

def playlist_song(name, artist, songs, n_songs=10):
    list_songs = find_similar(str(name), str(artist), songs, n_songs)

    if type(list_songs) != type(None):
        return list_songs

    return None

def recommendMusic(musicName):
    musicName = musicName.replace(", ", ",")
    musicName = musicName.split(',')
    recommendation = playlist_song(musicName[0], musicName[1], songs, 6)
    return recommendation

# print("Type the name of a song and the author: ", end="")
# song_name_input = input()
# recommendation = recommendMusic(song_name_input)
# print(recommendation)
# print(fromMusicTableToText(recommendation, 0))