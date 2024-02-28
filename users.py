from flask import Blueprint , render_template, request, redirect
from models import *
from models import Users, db, Song, Playlist
user_bp = Blueprint('user', __name__ )

@user_bp.route("/<username>/my_account")
def my_account(username):
    user = Users.query.get(username)
    playlists = Playlist.query.filter_by(created_by=username)
    return render_template('my_account.html',user=user,playlists=playlists)

@user_bp.route("/<username>/<int:song_id>/read_lyrics")
def read_lyrics(username,song_id):
    song = Song.query.get(song_id)
    user = Users.query.get(username)
    return render_template("read_lyrics.html",song=song,user=user)

@user_bp.route("/<username>/<int:song_id>/add_to_playlist",methods=["GET","POST"])
def add_to_palylist(username,song_id):
    song = Song.query.get(song_id)
    if request.method=="POST":
        playlist_name=request.form.get("playlist")
        playlist=Playlist.query.filter_by(Playlist_name=playlist_name)[0]
        playlist.songs.append(song)
        db.session.commit()
        return redirect(f"/{username}/home")
    user = Users.query.get(username)
    playlists = Playlist.query.filter_by(created_by=username)
    print(playlists)
    # print("somh")
    return render_template("add_to_playlist.html",user=user,playlists=playlists,song=song)

@user_bp.route("/<username>/<int:song_id>/create_new_playlist",methods=["GET","POST"])
def create_new_playlist(username,song_id):
    song = Song.query.get(song_id)
    user=Users.query.get(username)
    if request.method=="POST":
        name=request.form.get("name")
        p1=Playlist(Playlist_name=name,created_by=username)
        db.session.add(p1)
        db.session.commit()
        p1.songs.append(song)
        db.session.commit()
        return redirect(f"/{username}/home")
    return render_template("create_new_playlist.html",user=user,song=song)
@user_bp.route("/<username>/<playlist_id>/view")
def view_playlist(username,playlist_id):
    user=Users.query.get(username)
    playlist = Playlist.query.get(playlist_id)
    songs = playlist.songs
    return render_template('view_playlist.html',user=user,songs=songs,playlist=playlist)

@user_bp.route("/<username>/latest_songs")
def latest_songs(username):
    user=Users.query.get(username)
    songs=Song.query.all()
    return render_template("latest_songs.html",songs=songs,user=user)

@user_bp.route("/<username>/<int:song_id>/edit",methods=["GET","POST"])
def edit_song(username,song_id):
    user=Users.query.get(username)
    song=Song.query.get(song_id)
    if request.method=="POST":
        song_name=request.form.get("name")
        lyrics=request.form.get("lyrics")
        song.song_name=song_name
        song.lyrics=lyrics
        db.session.commit()
        return redirect(f'/{username}/{song_id}/read_lyrics')
    return render_template("edit_song.html",user=user,song=song)

@user_bp.route("/<username>/<int:song_id>/rate",methods=["GET","POST"])
def rate_song(username,song_id):
    user=Users.query.get(username)
    song=Song.query.get(song_id)
    if request.method=="POST":
        rating=float(request.form.get("rating"))
        prev_rating=song.rating
        reviews=song.reviews
        new_rating=(prev_rating*reviews+rating)/(reviews+1)
        new_rating=round(new_rating,2)
        song.rating=new_rating
        song.reviews=reviews+1
        db.session.commit()
        return redirect(f"/{user.username}/{song_id}/read_lyrics")
    return render_template("rating.html",user=user,song=song)