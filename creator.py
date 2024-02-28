from flask import Blueprint , render_template, request, redirect
from models import *
from models import Users, db, Song, Playlist
creator_bp = Blueprint('creator', __name__ )

@creator_bp.route("/<username>/become_creator",methods=["GET","POST"])
def become_creator(username):
    user = Users.query.get(username)
    if request.method=="POST":
        text = request.form.get("text")
        if text == "I AGREE":
            user.usertype=1
            db.session.commit()
            return redirect(f"/{username}/welcome_creator")
        else:
            return render_template("become_creator.html",status=1,user=user)
    return  render_template("become_creator.html",status=0,user=user)
@creator_bp.route("/<username>/welcome_creator")
def welcome_creator(username):
    user=Users.query.get(username)
    return render_template('welcome_creator.html',user=user)


@creator_bp.route("/<username>/creator",methods=['GET','POST'])
def creator(username):
    user=Users.query.get(username)
    if request.method=="POST":
        item = request.form.get("query")
        songs = Song.query.filter(Song.song_name.like('%'+item+'%'),Song.creator.like(username)).all()
        playlists = Playlist.query.filter(Playlist.Playlist_name.like('%'+item+'%'),Playlist.created_by.like(username)).all()
        # return item
        return render_template("search_creator.html",user=user,songs=songs,playlists=playlists,search=item)
    user=Users.query.get(username)
    songs = Song.query.filter_by(creator=username)
    playlists= Playlist.query.filter_by(created_by=username)
    return render_template("creator.html",user=user,songs=songs,playlists=playlists)

@creator_bp.route("/<username>/creator/add_song",methods=["GET","POST"])
def add_song(username):
    user = Users.query.get(username)
    if request.method=="POST":
        song_name = request.form.get("song_name")
        lyrics = request.form.get("lyrics")
        genre = request.form.get("genre")
        new_song = Song(song_name=song_name, creator=username, lyrics=lyrics,genre=genre,rating=0,reviews=0)
        db.session.add(new_song)
        db.session.commit()
        return redirect(f"/{username}/creator")
    return render_template("add_song.html",user=user)

@creator_bp.route("/<username>/creator/all_songs")
def all_songs_cre(username):
    songs=Song.query.filter_by(creator=username)
    user = Users.query.get(username)
    return render_template("all_songs.html",songs=songs,user=user)

@creator_bp.route('/<username>/<int:song_id>/delete')
def delete_song(username,song_id):
    user=Users.query.get(username)
    song=Song.query.get(song_id)
    db.session.delete(song)
    db.session.commit()
    playlists=song.playlists
    for playlist in playlists:
        if len(playlist.songs)==0:
            p=Playlist.query.get(playlist.id)
            db.session.delete(p)
            db.session.commit()
    return redirect("/<username>/latest_songs")
