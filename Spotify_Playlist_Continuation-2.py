#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''

Method: Run analysis on dataset.

Parameters: Playlist_dataset, Track_dataset

Body:

Shows charts and visualisations for the data in both datasets.
Histograms, distributions
Basic metrics

'''


# In[2]:


import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from collections import defaultdict
# import re
# import plotly.io as pio
# pio.renderers.default='notebook'


# In[21]:


get_ipython().system('pip3 install pandas')



def printCharts(playlists_df, mostPopularPlaylist, mostPopularTracks, mostPopularAlbums, mostPopularArtists):
    
    print ("Charts/Graphs: ")
    
    # Scatter - num_tracks
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=playlists_df.index, y=playlists_df['num_tracks'],
                        mode='markers',
                        name='markers'))
    fig.add_trace(go.Scatter(x=playlists_df.index, y=[playlists_df['num_tracks'].mean()] * playlists_df.size,
                        mode='lines',
                        name='lines'))
    
    fig.update_layout(
        title="Scatter plot for number of tracks in each playlist and mean",
        xaxis_title="Playlist index",
        yaxis_title="num_tracks")
    
    fig.show()

    # Scatter - num_albums
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=playlists_df.index, y=playlists_df['num_albums'],
                        mode='markers',
                        name='markers'))
    fig.add_trace(go.Scatter(x=playlists_df.index, y=[playlists_df['num_albums'].mean()] * playlists_df.size,
                        mode='lines',
                        name='lines'))

    fig.update_layout(
        title="Scatter plot for number of albums in each playlist and mean",
        xaxis_title="Playlist index",
        yaxis_title="num_albums")
    fig.show()

    # Histogram - num_edits
    fig = px.histogram(playlists_df, x="num_edits")
    fig.update_layout(
        title="Histogram of number of albums in the playlists",
        xaxis_title="num_albums bins",
        yaxis_title="occurence_count")
    fig.show()

    # Histogram - num_tracks
    fig = px.histogram(playlists_df, x="num_tracks")
    fig.update_layout(
        title="Histogram of number of tracks in the playlists",
        xaxis_title="num_tracks bins",
        yaxis_title="occurence_count")
    fig.show()

    # Histogram - num_followers
    fig = px.histogram(playlists_df, x="num_followers")
    fig.update_layout(
        title="Histogram of number of followers for the playlists",
        xaxis_title="num_followers bins",
        yaxis_title="occurence_count")
    fig.show()

    # Histogram - duration_ms
    fig = px.histogram(playlists_df, x="duration_ms")
    fig.update_layout(
        title="Histogram of duration (in ms) of the playlists",
        xaxis_title="duration (in ms) bins",
        yaxis_title="occurence_count")
    fig.show()

    # Scatter - Playlists with relation b/w duration_ms and num_followers (skewed as of now)
    fig = px.scatter(playlists_df, x=playlists_df.index, y='duration_ms', size="num_followers")
    fig.update_layout(
        title="Correlation of number of followers with duration (in ms) of the playlists",
        xaxis_title="playlist index",
        yaxis_title="duration_ms")
    fig.show()

    # Scatter - Most popular playlists
    fig = px.bar(mostPopularPlaylist[:20], x='name', y='num_followers')
    fig.update_layout(
        title="Most popular playlists",
        xaxis_title="playlist index",
        yaxis_title="num_followers")
    fig.show()

    # Scatter - Most Popular Tracks 
    fig = px.bar(mostPopularTracks[:20], x='track_name', y='popularity')
    fig.update_layout(
        title="Most popular tracks",
        xaxis_title="playlist index",
        yaxis_title="track popularity")
    fig.show()

    # Scatter - Most popular Albums
    fig = px.bar(mostPopularAlbums[:20], x='album_name', y='popularity')
    fig.update_layout(
        title="Most popular albums",
        xaxis_title="playlist index",
        yaxis_title="album popularity")
    fig.show()

    # Scatter - Most popular Artists
    fig = px.bar(mostPopularArtists[:20], x='artist_name', y='popularity')
    fig.update_layout(
        title="Most popular artists",
        xaxis_title="playlist index",
        yaxis_title="artist popularity")
    fig.show()


# In[3]:
def showDataAnalysis_new(playlists_df, tracks_df):
#     tracks = {}
    albums = {}
    artists = {}
    track_popularity = defaultdict(int)
    album_popularity = defaultdict(int)
    artist_popularity = defaultdict(int)


    for t in playlists_df['tracks']:
#         ts = t.split('\'')[1::2]
        for t_ in t:
#             tracks[t_['track_uri']] = t_
            track = tracks_df[tracks_df['track_uri'] == t_]
#             print (t_, track['artist_uri'])
#             print (track.iloc[0], type(track))
#             print ("S", track['artist_uri'])
            artists[track['artist_uri'].iloc[0]] = track.iloc[0]
            albums[track['album_uri'].iloc[0]] = track.iloc[0]
        
            track_popularity[t_] += 1
            album_popularity[track['album_uri'].iloc[0]] += 1
            artist_popularity[track['artist_uri'].iloc[0]] += 1

#     tracks_df = pd.DataFrame(tracks.values(), index=tracks.keys())
    artists_df = pd.DataFrame(artists.values(), index=artists.keys())
    albums_df = pd.DataFrame(albums.values(), index=albums.keys())
    
#     track_popularity = defaultdict(int)
#     album_popularity = defaultdict(int)
#     artist_popularity = defaultdict(int)

#     for i in playlists_df['tracks']:
#         for track in i:
#             track_popularity[track] += 1
#             album_popularity[tracks_df[tracks_df['track_uri'] == track]['album_uri'].iloc[0]] += 1
#             artist_popularity[tracks_df[tracks_df['track_uri'] == track]['artist_uri'].iloc[0]] += 1
            
    tracks_df['popularity'] = tracks_df['track_uri'].map(track_popularity)
    artists_df['popularity'] = artists_df['artist_uri'].map(artist_popularity)
    albums_df['popularity'] = albums_df['album_uri'].map(album_popularity)

    mostPopularPlaylist = playlists_df.sort_values(by='num_followers', ascending=False)
    mostPopularTracks = tracks_df.sort_values(by=['popularity'], ascending=False)
    mostPopularAlbums = albums_df.sort_values(by=['popularity'], ascending=False)
    mostPopularArtists = artists_df.sort_values(by=['popularity'], ascending=False)
    
    printCharts(playlists_df, mostPopularPlaylist, mostPopularTracks, mostPopularAlbums, mostPopularArtists)
    return playlists_df, mostPopularPlaylist, mostPopularTracks, mostPopularAlbums, mostPopularArtists


def loadPlaylistData(data):
    under_60_tracks_playlists = [playlist for playlist in data['playlists'] if 10 < playlist['num_tracks'] < 60]
    tracks = []
    for playlist in under_60_tracks_playlists:
        track_uris = []
        for track in playlist['tracks']:
            tracks.append(track)
            track_uris.append(track['track_uri'])
        playlist['tracks'] = track_uris
    p_df = pd.DataFrame(under_60_tracks_playlists)
    t_df = pd.DataFrame(tracks)
    return under_60_tracks_playlists, p_df, t_df


# In[5]:


all_playlists = pd.DataFrame()
all_tracks = pd.DataFrame()
L = []

for fileName in ['mpd.slice.122000-122999.json', 'mpd.slice.308000-308999.json', 'mpd.slice.582000-582999.json', 'mpd.slice.858000-858999.json', 'mpd.slice.995000-995999.json']:
    f = open(fileName)
    data = json.load(f)
    l, playlist_df, tracks_df = loadPlaylistData(data)
    # print(playlist_df)
    L.append(l)
    all_playlists = pd.concat([all_playlists, playlist_df])
    all_tracks = pd.concat([all_tracks, tracks_df])
    
# playlists_df1 = pd.concat(all_playlists)
# tracks_df1 = pd.concat(all_tracks)
all_tracks = all_tracks.drop_duplicates(subset=['track_uri'])
# all_tracks.set_index('track_uri')


a, b, c, d, e = showDataAnalysis_new(all_playlists, all_tracks)


