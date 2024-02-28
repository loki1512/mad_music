from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
association=db.Table('association',
    # db.Column('ass_id',db.Integer(),primary_key=True),
    db.Column('playlist_id',db.Integer(),db.ForeignKey('playlist.id')),
    db.Column('song_id',db.Integer(),db.ForeignKey('song.song_id')))
class Users(db.Model):
    username = db.Column(db.String(),primary_key=True)
    password = db.Column(db.String(),nullable=False)
    name = db.Column(db.String())
    email = db.Column(db.String())
    contact = db.Column(db.String())
    usertype = db.Column(db.Integer())
    flagged = db.Column(db.Integer())
    nickname = db.Column(db.String())
    songs = db.relationship("Song", backref= 'created_by', cascade = "all, delete")
    
class Song(db.Model):
    song_id = db.Column(db.Integer(),primary_key=True)
    song_name = db.Column(db.String(),nullable=False)
    creator = db.Column(db.String(),db.ForeignKey('users.username'))
    playlists = db.relationship("Playlist",secondary=association,backref='songs')
    genre = db.Column(db.String(),nullable=False)
    lyrics = db.Column(db.Text(),nullable=False)
    rating= db.Column(db.Float(5))
    reviews=db.Column(db.Integer())
    flagged = db.Column(db.Integer())
    
class Playlist(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    Playlist_name = db.Column(db.String(),nullable=False)
    created_by= db.Column(db.String(),db.ForeignKey('song.creator'))
    # songs = db.relationship("Song",secondary=association,backref="is_in",uselist=True)
    
    __table_args__ = (
        db.UniqueConstraint('Playlist_name', 'created_by', name='_playlist_name_created_by_uc'),
    )


