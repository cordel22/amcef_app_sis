###########        browser         ###########
import sqlite3
from typing import no_type_check
from bottle import route, run, debug, template, request, static_file, error, get, post, view, redirect, response, route

###########      RESTful api       ###########
import requests
###########        database         ##########
import db  
from sqlalchemy.orm import sessionmaker
import os


from misc import api_call, add_post, show_all, show_by_user, show_by_id, edit_title, edit_body, delete_by_id, delete_all

############         login         ###########
from sys import api_version
#   https://stackoverflow.com/questions/52461587/basic-auth-authentication-in-bottle
import uuid

##############     model       ###############

######### endpoints for the restful api ######
endpoint1 = 'users'
endpoint2 = 'posts'
#########   url of the restful api  ##########
url = "https://jsonplaceholder.typicode.com/"
##########  response variable array   ########

##########       dummy users          ########

users = [       #   admin first!!!  change  !!!
  { "id":"000",
    "name":"admin",
    "last_name":"admin",
    "email":"admin@admin.com",
    "password":"admin",
    "admin":"1" 
  },
  { "id":"001",
    "name":"a",
    "last_name":"aa",
    "email":"a@a.com",
    "password":"pass1",
    "admin":"0" 
  },
  { "id":"002",
    "name":"b",
    "last_name":"bb",
    "email":"b@b.com",
    "password":"pass2",
    "admin":"0" 
  }
]

##############  login sessions  ##############
sessions = {}



#################   control   ################


"""             put this to misc          """         # TODO: put this to misc
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

      result.append({"user_id" : s.user_id, "id" :  s.id, "title" : s.title, "body" : s.body, "date" : s.date})     #   TypeError('Object of type datetime is not JSON serializable')
    return result

    
########## query database by user_id ##########
def show_by_user(userId):
    result = []
    for t in session.query(db.Posts).filter(db.Posts.user_id==userId):

      result = {"user_id" : t.user_id, "id" :  t.id, "title" : t.title, "body" : t.body, "date" : t.date}
    return result

##########   query database by post id #########
def show_by_id(id):
    for u in session.query(db.Posts).filter(db.Posts.id==id):

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
  session.query(db.Posts).filter(db.Posts.id == identif).delete()
  session.commit()
############     delete all     ########### 
def delete_all():
  session.query(db.Posts).delete()
  session.commit()

############   authentication   ###########
def is_authenticated_user(user_email, user_password):
    for user in users:
      if user_email == user["name"] and user_password == user["password"]:
        return True
      return False

"""       end of put this to misc          """         # TODO: end of put this to misc



##############################################
#creating, connecting and populating database#

###### create database if there is none  ##### 
os.system('python db.py')

#######  connect to database session  ########
Session = sessionmaker(bind=db.engine)
session = Session()

####     download posts from api server  #####
####  check if the database has any data  ####
########  if the database is empty    ########
########    fill it in from server    ########
if len(show_all()) < 1:
  res = api_call(url, endpoint2)                  # condition only if db empty!!!
# saves the posts from api into the database #
  for x in range(len(res)):
    add_post(
      res[x]["userId"],
      res[x]["id"],
      res[x]["title"],
      res[x]["body"]
      )


##############################################
############        view          ############


###########         home           ###########

@get("/")
@view("home")
def _():
  return


#########           login          ###########

@get("/login")
@view("login")
def _():
  #########     users from RESt server  ########
  res = api_call(url, endpoint1)
  return  dict(res=res)

#########           post           ###########

@post("/login")
def _():
  user_email = request.forms.get("user_email")
  user_password = request.forms.get("user_password")
#########     users from RESt server  ########
  res = api_call(url, endpoint1)


######    testing for embedded users    ######
  for user in users:

    if user_email == user["email"] and user_password == user["password"]:
      user_session_id = str(uuid.uuid4())
      sessions[user_session_id] =  user # maybe without password
      response.set_cookie("user_session_id", user_session_id)
      
      # admin login condition
      if user["admin"] == "1":
          # redirect to admin if admin                  #   TODO: set the redirections according to admin attribute
          return redirect("/admin")
      else:
      # redirect to forum
        return redirect("/forum")

######    testing for users from server    ######
  
  for x in range(len(res)):
    ########    CAREFULL! WE DONT HAVE PASSWORD ON SERVER!!!   USE NAME!!  #######
    if user_email == res[x]["email"] and user_password == res[x]["name"]:
      user_session_id = str(uuid.uuid4())
      sessions[user_session_id] =  res[x] # maybe without password
      response.set_cookie("user_session_id", user_session_id)
    
      #######      no admins      ######
      #######   redirect to forum  ######
      return redirect("/forum")
  # redirect to login when authentication failed
  return redirect("/login")

#########           logout            ##########

@get("/logout")
def _():
  user_session_id = request.get_cookie("user_session_id")
  sessions.pop(user_session_id)
  ##### miscellaneous   #####
  print("#"*30)
  print(sessions)
  ##### miscellaneous   #####
  return redirect("/login")




#########  admin   ###########
####  accesses everything ####

@route('/admin')
def admin():
    
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_session_id = request.get_cookie("user_session_id")
    # if user is not admin, which is only in embedded ones..    #   TODO: set the redirections according to admin attribute

    #     miscellaneous   ###
    ####  see if user in session has admin attribute  ###
    
    if 'address' in sessions[user_session_id]:
    ###   see if admin attribute is eual to zero
      # if sessions[user_session_id]["admin"] == "0":
  #       # redirect to forum if not admin                  #   TODO: set the redirections according to admin attribute
      return redirect("/forum")
  #       print("miscellaneous")
    
    #     miscellaneous   ###
    #########   redirected to forum a if not logged in, forum will redrect to login back

    user = sessions[user_session_id]
    # return dict(user=user)
    result = show_all()
    output = template('admin', dict(user=user), rows=result)
    return output



##########   all database items   ##########
@route('/forum')
def forum():

    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_session_id = request.get_cookie("user_session_id")
    if user_session_id not in sessions:
      return redirect("/login")
    user = sessions[user_session_id]
    # return dict(user=user)
    result = show_all()
    output = template('make_table', dict(user=user), rows=result)
    return output


######   all database items api service   ######
@get('/forumapi')
def forumapi():
    
    return str(show_all())


#############  adding a new post #############
@route('/new/<no:int>', method='GET')
def new_item(no):
    if request.GET.save:
      
      new_title = request.GET.title.strip()
      new_body = request.GET.body.strip()

      add_user_id = no                        #   TODO: 001 zapise ako 1...
      ########  last post's id + 1 #####
      posts_list = show_all()
      if len(posts_list) > 0:
        last_id = posts_list[len(posts_list)-1]["id"]
        add_id = last_id + 1
      else:
        add_id = 1
      

      add_title = new_title
      add_body = new_body
      add_post(add_user_id, add_id, add_title, add_body)
      return '<p>The new task was inserted into the database, the ID is %s, <a href="/admin">back to posts</a></p>' % add_id
      # return str(new)
    else:
        return template('new_task.tpl', no=no)

#############  edditing a post #############

@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        
        edited_title = request.GET.get("title", 1)
        edited_body = request.GET.get("body", 1)
        
        id = no
        newTitle = edited_title
        newBody = edited_body
        edit_title(id, newTitle)
        edit_body(id, newBody)
        
        return '<p>The item number %s was successfully updated <a href="/admin">back to posts</a></p>' % no
    else:
        
        cur_data = show_by_id(no)

        return template('edit_task', old=cur_data, no=no)

#############  deleting a post #############            # TODO: preco???
# @route('/del_post/<no:int>', method='GET')
@route('/del_post/<no:int>', method='GET')
def del_post(no):
    
    delete_by_id(no)
    return redirect('/admin')
    # return '<p>Congrats, you just deleted post of ID %s</p>' % no

#############  deleting all posts #############

@route('/del_all')
def del_all():
    delete_all()
    return '<p>Congrats, you just emptied the database:) <a href="/admin">back to posts</a></p>'
#############  help page #############

@route('/help')
def help():
    return static_file('help.html', root='.')

#############  error routes #############

@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

run(port=8080, host='127.0.0.1', reloader=True)