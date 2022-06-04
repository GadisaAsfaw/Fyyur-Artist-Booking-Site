#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from enum import unique
import json
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app,db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  areas = Area.query.all()

  #select only areas that have vanues
  filtered_data  = list(filter(lambda area: area.venues !=[], areas))

  data = [
      {
        "city":area.city,
        "state":area.state,
        "venues":[
          {
            "id":venue.id,
            "name":venue.name,
            "num_upcoming_shows":len(list(filter(lambda show: show.start_time >= datetime.now(), venue.shows)))
            
          } for venue in area.venues],

      }   for area in filtered_data]
 
  return render_template('pages/venues.html', areas=filtered_data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
  realdata = {
    "count":venues.count(),
    "data":[
      {
        "id":venue.id,
        "name":venue.name,
        "num_upcoming_shows":len(list(filter(lambda show: show.start_time >= datetime.now(), venue.shows)))
      } for venue in venues]
  }
  
  return render_template('pages/search_venues.html', results=realdata, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.get(venue_id)
  genres_name= [genre.name for genre in venue.genres]

  past_shows = list(filter(lambda show: show.start_time < datetime.now(), venue.shows))
  upcoming_shows = list(filter(lambda show: show.start_time >= datetime.now(), venue.shows))
  
  realdata ={
      "id":venue.id,
      "name":venue.name,
      "genres":genres_name,
      "address":venue.address,
      "city":venue.area.city,
      "state":venue.area.state,
      "phone":venue.phone,
      "website":venue.website,
      "facebook_link":venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description":venue.seeking_description,
      "image_link":venue.image_link,
      "past_shows":[
        {
          "artist_id":show.artist.id,
          "artist_name":show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": show.start_time 
          } for show in past_shows],
      "upcoming_shows": [
         {
          "artist_id":show.artist.id,
          "artist_name":show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": show.start_time 
          } for show in upcoming_shows],
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
      
           
    }
  
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=realdata)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  form = VenueForm(request.form)
  #print(form.genres.data)
  
 
  error = False
  try:
      genres = []
       #If genre doesn't exist create one
      for name in form.genres.data:
        genre = Genre.query.filter_by(name=name).first()
        if genre is None:
          genres.append(Genre(name=name))
        else:
          genres.append(genre)

      
      area = Area.query.filter_by(city=form.city.data,state=form.state.data).first()

      #If area does not exist create one
      if area is None:
        area =  Area(city=form.city.data,state=form.state.data)

      venue = Venue(name=form.name.data,address=form.address.data,phone=form.phone.data,image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,seeking_talent=form.seeking_talent.data,
                    website =form.website_link.data, seeking_description=form.seeking_description.data)
      

      for genre in genres:
        venue.genres.append(genre)
      
      venue.area = area
      db.session.add(area)
      db.session.commit()
      
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
     error = True
     db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    
  else:
      return render_template('pages/home.html')
  
  
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)
    for show in venue.shows:
      db.session.delete(show)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists = Artist.query.all()
  realdata=[]
  
  #filter data
  for artist in artists:
    data ={"id":artist.id,"name":artist.name}
    realdata.append(data)

  return render_template('pages/artists.html', artists=realdata)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
  
  #filter data
  realdata = {
    "count":artists.count(),
    "data":[
      {
        "id":artist.id,
        "name":artist.name,
        "num_upcoming_shows":len(list(filter(lambda show: show.start_time >= datetime.now(), artist.shows)))
      } for artist in artists]
  }
  
  return render_template('pages/search_artists.html', results=realdata, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id 
  # TODO: replace with real artist data from the artist table, using artist_id
  
  artist = Artist.query.get(artist_id)
  genres_name= [genre.name for genre in artist.genres]

  past_shows  = list(filter(lambda show: show.start_time < datetime.now(), artist.shows))
  upcoming_shows= list(filter(lambda show: show.start_time >= datetime.now(), artist.shows))

  realdeta ={
     "id":artist.id,
     "name":artist.name,
     "genres":genres_name,
     "city":artist.area.city,
     "state":artist.area.state,
     "phone":artist.phone,
     "website":artist.website,
     "facebook_link":artist.facebook_link,
     "seeking_venue":artist.seeking_venue,
     "seeking_description":artist.seeking_description,
     "image_link":artist.image_link,
     "past_shows": [
        {
          "venue_id":show.venue_id,
          "venue_name":show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": show.start_time
        } for show in past_shows ],
     "upcoming_shows": [
        {
          "venue_id":show.venue_id,
          "venue_name":show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": show.start_time
        } for show in upcoming_shows],
     "past_shows_count": len(past_shows),
     "upcoming_shows_count": len(upcoming_shows),
   }
  
  return render_template('pages/show_artist.html', artist=realdeta)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  #filtered data
  #artis_data ={"id":artist.id,"name":artist.name}

  form.name.data = artist.name
  form.city.data = artist.area.city
  form.state.data = artist.area.state
  form.phone.data = artist.phone
  form.genres.data = [genre.name for genre in artist.genres]
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description


  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  error = False
  try:
    genres = []
       #If genre doesn't exist create one
    for name in form.genres.data:
      genre = Genre.query.filter_by(name=name).first()
      if genre is None:
        genres.append(Genre(name=name))
      else:
        genres.append(genre)

      
    area = Area.query.filter_by(city=form.city.data,state=form.state.data).first()
      #If area does not exist create one
    if area is None:
      area =  Area(city=form.city.data,state=form.state.data)


    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.area = area
    artist.phone = form.phone.data
    artist.genres = genres
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    db.session.commit()
  except:
     error = True
     db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()
  venue = Venue.query.get(venue_id)

  #filtered data
  #venue_data ={"id":venue.id,"name":venue.name}

  form.name.data = venue.name
  form.city.data = venue.area.city
  form.state.data = venue.area.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = [genre.name for genre in venue.genres]
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website_link.data = venue.website
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  error = False
  try:
    genres = []
    #If genre doesn't exist create one
    for name in form.genres.data:
      genre = Genre.query.filter_by(name=name).first()
      if genre is None:
        genres.append(Genre(name=name))
      else:
        genres.append(genre)

      
    area = Area.query.filter_by(city=form.city.data,state=form.state.data).first()
    #If area does not exist create one
    if area is None:
      area =  Area(city=form.city.data,state=form.state.data)


    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.area = area
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = genres
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
  except:
     error = True
     db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  #print(request.form)
  error = False
  try:
      genres = []
      for name in form.genres.data:
        genre = Genre.query.filter_by(name=name).first()
        if genre is None:
          genres.append(Genre(name=name))
        else:
          genres.append(genre)

      #If area does not exist create one
      area = Area.query.filter_by(city=form.city.data,state=form.state.data).first()
      if area is None:
        area =  Area(city=form.city.data,state=form.state.data)

      artist = Artist(name=form.name.data,phone=form.phone.data,image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,website=form.website_link.data,seeking_venue=form.seeking_venue.data,
                    seeking_description=form.seeking_description.data)
      #venue.genres=genres
      for genre in genres:
        artist.genres.append(genre)
      artist.area = area
      db.session.add(area)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
     error = True
     db.session.rollback()
  finally:
    db.session.close()
  if error == True:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    
  else:
      return render_template('pages/home.html')
  
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  real_data = Show.query.all()
  filtered_data = [
    {
     "venue_id":show.venue_id,
     "venue_name":show.venue.name,
     "artist_id":show.artist_id,
     "artist_name":show.artist.name,
     "artist_image_link":show.artist.image_link,
     "start_time":show.start_time
      #"start_time":format_datetime(str(show.start_time))
    } for show in real_data]
  
  return render_template('pages/shows.html', shows=filtered_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  error = False
  try: 
    if Venue.query.get(int(form.venue_id.data)) is None or Artist.query.get(int(form.artist_id.data)) is None:
      flash("ID doesn't exist!, Please refer back to Artist's or Venue's page! ")
      return render_template('pages/home.html')

    show = Show(start_time=form.start_time.data,venue_id=int(form.venue_id.data),artist_id=int(form.artist_id.data))
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
  finally:
   db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
