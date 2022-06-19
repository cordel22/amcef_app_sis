requires installed python3,
https://www.python.org/downloads/

sqlite
https://sqlite.org/download.html

from command line install dependencies: 
sqlalchemy
https://www.sqlalchemy.org
pip install sqlalchemy

bottle
https://bottlepy.org
pip install bottle

request
https://pypi.org › project › requests
pip install request

launch virtual environment from command line
./Scripts/activate

launch the app still from command line:
./python app.py

the app runs on bottle embedded server
127.0.0.1:8080

database is automatically created if not yet present in the root directory

if database is empty, it fills up from the RESTful API server

app allows 2 ways of login;

as an admin, with all the privileges
email:  admin@admin.com
name:   admin     
note: actually in case of embedded user, we compare to the password, in this case the same as name; 'admin'.

as a user, allows edit and delete of one's own messages
possible users are from the REST server