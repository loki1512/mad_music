from flask import request, render_template, Flask,redirect,Blueprint
from models import *
from models import Users, db, Song, Playlist

playlist_bp = Blueprint('playlists',__name__)

@playlist_bp.route("/<username>/create_playlist",methods=["GET","POST"])
def create_playlist(username):
    user=Users.query.get(username)
    if request.method=="POST":
        name=request.form.get("name")
        return redirect(f"/{username}/create_playlist/{name}/add_songs")
    return render_template("name_playlist.html",user=user)
@playlist_bp.route("/<username>/create_playlist/<name>/add_songs",methods=["GET","POST"])
def add_songs(username,name):
    user=Users.query.get(username)
    songs=Song.query.all()
    if request.method=="POST":
        song_ids = request.form.getlist("song_ids")
        playlist = Playlist(Playlist_name=name,created_by=username)
        db.session.add(playlist)
        db.session.commit()
        for song_id in song_ids:
            id = int(song_id)
            song = Song.query.get(id)
            if song not in playlist.songs:
                playlist.songs.append(song)
        db.session.commit()
        return redirect(f"/{username}/{playlist.id}/view")
    return render_template('add_songs_playlist.html',user=user,name=name,songs=songs)


@playlist_bp.route("/<username>/<playlist_id>/delete_playlist")
def delete_playlist(username,playlist_id):
    user = Users.query.get(username)
    playlist = Playlist.query.get(playlist_id)
    if(playlist.created_by==user.username or user.usertype==2):
        db.session.delete(playlist)
        db.session.commit()
    return redirect(f"/{username}/playlists")
@playlist_bp.route("/<username>/creator_playlists")
def creator_playlists(username):
    user=Users.query.get(username)
    playlists=Playlist.query.filter_by(created_by=username)
    return render_template("all_playlists.html",playlists=playlists,user=user)
    
