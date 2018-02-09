import pprint
import sys
import os
import subprocess

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

spotipy_client_id = '7acdfaeab02d443f82661f4a20d947e1'
spotipy_client_secret = '73f22e975ea84dcdb7ccba4bc82643c6'
spotipy_redirect_url = 'https://www.google.com/'

client_credentials_manager = SpotifyClientCredentials(client_id='7acdfaeab02d443f82661f4a20d947e1', client_secret='73f22e975ea84dcdb7ccba4bc82643c6')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_song():
	pass

def search_artist(artist,num_of_songs):
	#artist is a string containing artist name
	#returns a tuple containing a list of tracks and a list of track ids by each artist
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	results = sp.search(q = artist, limit = num_of_songs)
	artist_tracks = []
	track_ids = []
	for i,t in enumerate(results['tracks']['items']):
		track_ids.append(t['id'])
		artist_tracks.append(t['name'])
	return (artist_tracks,track_ids)

def get_playlist_tracks_artist(artists,num_of_songs):
	#artists is a list of artists
	#returns a tuple containing a list of tracks of all artists and a list of track ids for all of those tracks
	playlist_tracks = []
	track_ids = []
	for i in artists:
		artist_tracks, tracks = search_artist(i,num_of_songs)
		playlist_tracks.extend(artist_tracks)
		track_ids.extend(tracks)
	return (playlist_tracks, track_ids)

def search_genre():
	pass 

def get_tracks(track_ids):
	track_list = sp.tracks(track_ids)
	return track_list

def create_playlist(username, playlist_name):
	chosen_scope = 'playlist-modify-private'
	token = util.prompt_for_user_token(username, scope = chosen_scope, client_id = spotipy_client_id, client_secret = spotipy_client_secret, redirect_uri = spotipy_redirect_url)
	if token:
		sp = spotipy.Spotify(auth = token)
		sp.trace = True
		public = False
		playlist = sp.user_playlist_create(username, playlist_name, public = False)
		playlist_id = playlist.get('id')
		return playlist_id
	else:
		print("Can't get token for", username)

def add_tracks(username, playlist_id, track_ids):
	chosen_scope = 'playlist-modify-private'
	token = util.prompt_for_user_token(username, scope = chosen_scope, client_id = spotipy_client_id, client_secret = spotipy_client_secret, redirect_uri = spotipy_redirect_url)
	if token:
		sp = spotipy.Spotify(auth = token)
		sp.trace = True
		public = False
		sp.user_playlist_add_tracks(username,playlist_id, track_ids)
	else:
		print("Can't get token for", username)

def get_party_values(track_ids):
	results = sp.audio_features(track_ids)
	party_tracks = {}
	for i in results:
		result = i
		acoustic = result.get('acousticness')
		dance = result.get('danceability')
		energy = result.get('energy')
		track_id = result.get('id')
		party_value = (dance + energy) - acoustic
		real_party_value = round(party_value,3)
		party_tracks[real_party_value] = track_id
	return party_tracks

def party_organizer(party_tracks):
	party_values = list(party_tracks.keys())
	a = sorted(party_values, reverse = False)
	b = a[::2]
	c = a[-2::-2]
	party_values = b + c
	track_id_list = []
	for i in party_values:
		value = party_tracks[i]
		track_id_list.append(value)
	party_track_list = get_tracks(track_id_list)
	return track_id_list,party_track_list

def party_playlist():
	print("Welcome to the Party Playlist Maker!")
	print("We're going to make a playlist that is perfect for your next party!")
	print("-------------------------------------------------------------------")
	print("")
	response = input("First, how would you like to make this playlist, by songs, by artists, or by genres?: ")
	print('')


	if response.lower() == 'genres' or response.lower() == 'genre' or response.lower() == 'g':
		print("Okay cool! We're going to be making you a playlist based on your favorite genres!")
		print("The playlist will be made based on the top songs in the genre(s) that you pick!")
		print('')
		playlist_length = int(input("How many songs do you want in this playlist?: "))
		print('')
		genres = []
		i = 0
		while i < 2:
			if i == 0:
				genre = input("Awesome! What do you want to be the first genre in the playlist?: ")
				print('')
				genres.append(genre)
			i = 1
			if i == 1:
				response = input("Do you have another genre you would like in your playlist? (Yes or No): ")
				print('')
				if response.lower() == 'yes' or response.lower() == 'y':
					genre = input("What other artist would you like?: ")
					print('')
					if genre in genres:
					    genre = input("Oops! You already said that genre! What other genre would you like?: ")
					    print('')
					    genres.append(genre)
					genres.append(genre)
				if response.lower() == 'no' or response.lower() == 'n':
					break


	if response.lower() == 'artists' or response.lower() == 'artist' or response.lower() =='a':
		print("Okay cool! We're going to be making you a playlist based on your favorite artists!")
		print('')
		playlist_length = int(input("How many songs do you want in this playlist?: "))
		print('')
		artists = []
		i = 0
		while i < 2:
			if i == 0:
				artist = input("Awesome! Who do you want to be the first artist in the playlist?: ")
				print('')
				artists.append(artist)
			i = 1
			response = input("Do you have another artist you would like in your playlist? (Yes or No): ")
			print('')
			if response.lower() == 'yes' or response.lower() == 'y':
				artist = input("What other artist would you like?: ")
				print('')
				if artist in artists:
				    artist = input("Oops! You already said that artist! What other artist would you like?: ")
				    print('')
				    artists.append(artist)
				artists.append(artist)
			if response.lower() == 'no' or response.lower() == 'n':
				break
		num_of_artists = len(artists)
		num_of_songs = playlist_length//num_of_artists
		playlist_tracks, track_ids = get_playlist_tracks_artist(artists,num_of_songs)
		j = 1
		print("These are all the tracks that will be in your playlist:")
		for i in playlist_tracks:
			print(j,' ', i)
			j += 1
		print('')


	if response.lower() == 'songs' or response.lower() == 'song' or response.lower() == 's':
		print("Okay cool! We're going to be making you a playlist based on your favorite songs!")
		print('')
		playlist_length = int(input("How many songs do you want in this playlist?: "))
		print('')
		response2 = input("Do you want to manually enter songs (m) or make the playlist based off of your most listened tracks(t)?: ")
		print('')

		if response2.lower() == 'manually' or response2.lower() == 'm':
			num = playlist_length
			tracks = []
			while num > 0:
				if num == playlist_length:
					song = input("What do you want to be the first song in the playlist?: ")
					print('')
					songs.append(song)
				else:
					song = input("What other song would you like? (Enter 'Done' if you don't have any more songs): ")
					print('')
					if song.lower() == 'done':
						break
					else:
						songs.append(song)
                                num -= 1
                        j = 1
                        print("These are all the tracks that will be in your playlist:")
                        for i in tracks:
                                print(j,' ', i)
                                j += 1
                        print('')
		if response2.lower() == 'tracks' or response2.lower() == 't':
			print('Okay! Hold on while I make your party playlist for you')
			print('')

	username = input("What is your spotify username?: ")
	playlist_name = input("What would you like to name the playlist?: ")
	new_playlist = create_playlist(username, playlist_name)
	answer = input("Would you like your playlist categorized for maximum party awesomeness? (Y or N): ")
	print('')
	if answer.lower() == 'y':
		print("Cool! It'll just be a little longer before you're awesome playlist is finished!")
		party_tracks = get_party_values(track_ids)
		track_ids, track_list = party_organizer(party_tracks)
		add_tracks(username, new_playlist, track_ids)
		print("You're playlist has been made!")
		print('')
		print('Thanks for using my program!')
	if answer.lower() == 'n':
		print("Okay! You're playlist is being made!")
		add_tracks(username, new_playlist, track_ids)
		track_list = get_tracks(track_ids)
		print("You're playlist has been made!")
		print('')
		print('Thanks for using my program!')

party_playlist()
