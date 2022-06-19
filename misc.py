###########        browser         ###########
import sqlite3
from bottle import route, run, debug, template, request, static_file, error, get, post, view, redirect, response, route

###########      RESTful api       ###########
import requests

###########        database         ##########
import db  
from sqlalchemy.orm import sessionmaker
import os

#######  connect to database session  ########
Session = sessionmaker(bind=db.engine)
session = Session()

#######   calling restful api service   ######
def api_call(url, endpoint):
  return requests.get(url + endpoint).json()

###########   add post to database  ##########
def add_post(user_id, id, title, body):
    post = db.Posts( user_id, id, title, body)
    
    session.add(post)
    session.commit()

###########   query entire database ##########
def show_all():
    result = []
    for s in session.query(db.Posts).all():
      # print("\nuser_id : ", s.user_id, "\nid : ", s.id, "\ntitle : ", s.title, "\nbody : ", s.body, "\ndate : ", s.date)
      result.append({"user_id" : s.user_id, "id" :  s.id, "title" : s.title, "body" : s.body, "date" : s.date})     #   TypeError('Object of type datetime is not JSON serializable')
      # result.append({"user_id" : s.user_id, "id" :  s.id, "title" : s.title, "body" : s.body})
      # print(result)   ti vyhodi na stranku, ne do konzoly
    return result

    
########## query database by user_id ##########
def show_by_user(userId):
    result = []
    for t in session.query(db.Posts).filter(db.Posts.user_id==userId):
      # print("\nuser_id : ", t.user_id, "\nid : ", t.id, "\ntitle : ", t.title, "\nbody : ", t.body, "\ndate : ", t.date)
      result = {"user_id" : t.user_id, "id" :  t.id, "title" : t.title, "body" : t.body, "date" : t.date}
    return result

##########   query database by post id #########
def show_by_id(id):
    for u in session.query(db.Posts).filter(db.Posts.id==id):
      # print("\nuser_id : ", u.user_id, "\nid : ", u.id, "\ntitle : ", u.title, "\nbody : ", u.body, "\ndate : ", u.date)
      result = {"user_id" : u.user_id, "id" :  u.id, "title" : u.title, "body" : u.body, "date" : u.date}
    return result

#########   update post title   ##########
def edit_title(idecko, newTitle):
  session.query(db.Posts).filter(db.Posts.id == idecko).update({db.Posts.title:newTitle})
  session.commit()
##########   update post body   ##########
def edit_body(ident, newBody):
  session.query(db.Posts).filter(db.Posts.id == ident).update({db.Posts.body:newBody}, synchronize_session = False)
  session.commit()

###########   delete by id      ##########
def delete_by_id(identif):
  # session.query(db.Posts).filter(db.Posts.id == identif)
  # session.delete()
  session.query(db.Posts).filter(db.Posts.id == identif).delete()
  session.commit()
#   delete all
def delete_all():
  
  session.query(db.Posts).delete()
  session.commit()

