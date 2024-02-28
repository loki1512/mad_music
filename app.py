from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from models import db,Users, Song, Playlist
from creator import creator_bp
from users import user_bp
from playlists import playlist_bp
from sqlalchemy import func
from collections import Counter
# from user import *
app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
primary_user = None
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_test_db.sqlite3' 
sessi = Session()
sessi.init_app(app)
db.init_app(app)
app.app_context().push()

@app.route("/")
def lander():
    return render_template("landingpage.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            user = Users.query.get(username)
            if(user.password == password):
                print("yes")
                primary_user=user
                session['user'] = primary_user.username
                return redirect(f"{username}/home")
            else:
                return render_template("login.html",status=1)
        except:
            # print('exr')
            return render_template("login.html",status=1)
        
    return render_template("login.html",status=0)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        contact = request.form.get("contact")
        nickname = request.form.get("nickname")
        usertype=0
        new_user = Users(username=username,password=password,email=email,contact=contact,nickname=nickname,usertype=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(f"/{username}/home")
    return render_template("register.html")
    
@app.route("/<username>/home",methods=["GET","POST"])
def home(username):
    user = Users.query.get(username)
    if user.usertype==2:
        return redirect("/admin")
    if request.method=="POST":
        item = request.form.get("query")
        songs = Song.query.filter(Song.song_name.like('%'+item+'%')).all()
        playlists = Playlist.query.filter(Playlist.Playlist_name.like('%'+item+'%')).all()
        return render_template("search.html",user=user,songs=songs,playlists=playlists,search=item)
    user = Users.query.get(username)
    songs = Song.query.all()
    songs = songs[-5::]
    songs_rating = Song.query.order_by(Song.rating.desc()).limit(5).all()
    songs=songs[::-1]
    playlists=Playlist.query.all()
    playlists=playlists[-4:]
    playlists=playlists[::-1]
    return render_template("home.html",user=user,songs=songs,playlists=playlists,songs_rating=songs_rating)

@app.route("/<username>/my_space")
def myspace(username):
    user = Users.query.get(username)
    return render_template("my_space.html",user=user)

@app.route("/<username>/playlists",methods=["GET","POST"])
def playlists(username):
    user = Users.query.get(username)
    playlists=Playlist.query.all()
    return render_template('all_playlists.html',playlists=playlists,user=user)



@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect("/login")

app.register_blueprint(creator_bp)
app.register_blueprint(user_bp)
app.register_blueprint(playlist_bp)

@app.route("/admin")
def admin_dash():
    users=Users.query.count()
    playlists=Playlist.query.count()
    songs=Song.query.count()
    genres = db.session.query(Song.genre).all()
    genre_counter = Counter(genre[0] for genre in genres)
    mode = genre_counter.most_common(1)[0][0]
    return render_template('admin_dashboard.html',users=users,playlists=playlists,songs=songs,mode=mode)
@app.route('/users')
def user_management():
    users = Users.query.all()  # Retrieve all users from the database
    return render_template('users.html', users=users)
@app.route('/admin/<username>/view_user')
def view_user(username):
    user=Users.query.get(username)
    playlists=Playlist.query.filter_by(created_by=username)
    songs=user.songs
    return render_template('view_user.html',user=user,playlists=playlists,songs=songs)
@app.route("/admin/<int:song_id>/flag")
def flag_song(song_id):
    song=Song.query.get(song_id)
    if(song.flagged==1):
        song.flagged=0
    else:
        song.flagged=1
    db.session.commit()
    return redirect(f"/admin/{song_id}/read_lyrics")
@app.route("/admin/<username>/flag_user")
def flag_user(username):
    user=Users.query.get(username)
    if(user.flagged==1):
        user.flagged=0
    else:
        user.flagged=1
    db.session.commit()
    return redirect(f"/admin/{username}/view_user")
@app.route("/admin/<username>/delete_user")
def delete_user(username):
    user=Users.query.get(username)
    db.session.delete(user)
    db.session.commit()
    return redirect(f"/users")

if __name__ == "__main__":
    app.run(debug=True)
    

