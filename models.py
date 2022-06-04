from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class Show(db.Model):
    __tablename__ = 'shows'
    id =    db.Column(db.Integer, primary_key=True,autoincrement=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('venues.id'), primary_key=True)
    artist_id = db.Column(db.Integer,db.ForeignKey('artists.id'), primary_key=True)
    start_time = db.Column(db.DateTime,nullable=False)
    venue = db.relationship('Venue', backref=db.backref("shows", cascade="all, delete-orphan"))
    artist = db.relationship('Artist', backref=db.backref("shows", cascade="all, delete-orphan"))
    def __repr__(self):
      return f'<Show:{self.id}, AD:{self.artist_id}, VA:{self.venue_id} show-time:{self.start_time}>'

class Area(db.Model):
    __tablename__ = 'areas'
    id =    db.Column(db.Integer, primary_key=True)
    city =  db.Column(db.String(), nullable=False)
    state = db.Column(db.String(),nullable=False)
    venues = db.relationship('Venue', backref='area', lazy=True)####
    artists = db.relationship('Artist', backref='area', lazy=True)####
    def __repr__(self):
      return f'<Area:{self.id}, state:{self.state}, city:{self.city}>'

venuegenres = db.Table('venuegenres',
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)
artistgenres = db.Table('artistgenres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)
class Genre(db.Model):
    __tablename__ = 'genres'
    id =    db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(),unique=True,nullable=False)
    def __repr__(self):
      return f'<Genre:{self.id}, {self.name}>'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500),nullable=False)
    #city = db.Column(db.String(120))
    #state = db.Column(db.String(120))
    address = db.Column(db.String(300))
    phone = db.Column(db.String(120), unique=True)
    image_link = db.Column(db.String(500),unique=True)
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500),default="We are looking for Talent")
    genres = db.relationship('Genre',secondary=venuegenres , lazy='subquery',backref=db.backref('venues', lazy=True))####
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'),
                        nullable=False)
    artists = db.relationship("Artist", secondary="shows")

    def __repr__(self):
      return f'<Venue:{self.id}, {self.name}, AID:{self.area_id}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    #city = db.Column(db.String(120))
    #state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500),default="I am looking for Venues")
    genres = db.relationship('Genre',secondary=artistgenres , lazy='subquery',backref=db.backref('artists', lazy=True))####
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'),
                        nullable=False)
    venues = db.relationship("Venue", secondary="shows")
    def __repr__(self):
      return f'<Artist:{self.id}, {self.name}, AID:{self.area_id}>'


