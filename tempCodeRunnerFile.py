if request.method=="POST":
        item = request.form.get("query")
        songs = Song.query.filter(Song.song_name.like('%'+item+'%')).all()
        playlists = Playlist.query.filter(Playlist.Playlist_name.like('%'+item+'%')).all()
        return render_template("search.html",user=user,songs=songs,playlists=playlists,search=item)