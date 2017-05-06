# Multi User Blog

A project by Christopher Stieg for the **Intro to Backend** course,
which is part of the **Full Stack Nanodegree** from
[Udacity.com](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
Based on the Google Cloud App Engine platform, it is a website that allows users
to sign up, login, and compose blog entries.  Logged in users can also comment on
blog entries, like entries or comments by other users, and edit or delete their
own entries and comments.

## Components
### Configuration Files
* _app.yaml_ contains configuration information for Google App Engine to be able
to find the folders and files to run the app.
* _index.yaml_ contains a list of the indexes to be created

### Python Backend
* _main.py_ is the entry point of the app and contains the URL routing information.
#### Handlers Module
* _addcomment.py_ adds a comment to a particular blog entry.
* _compose.py_ composes a new blog entry.
* _deletecomment.py_ deletes a comment on a blog entry.
* _deletepost.py_ deletes a particular blog entry.
* _editcomment.py_ edits a particular comment on a blog entry.
* _editpost.py_ edits a particular blog entry.
* _handler.py_ contains the base handler class which extends the webapp2 handler,
and is extended by each of the other handlers. It also has decorators to check
the validity of HTTP calls to the handlers, as well as other miscellaneous functions.
* _likecomment.py_ likes a particular comment on a blog entry.
* _likepost.py_ likes a particular blog entry.
* _login.py_ logs in a registered user.
* _logout.py_ logs out a registered user.
* _mainpage.py_ displays the main page or a particular blog entry.
* _signup.py_ registers a user to participate on the blog.
#### Models Module
* _blogentry.py_ contains the class representing the blog entries.
* _comment.py_ contains the class representing comments on the blog entries,
as well as functions to manipulate them.
* _commentlike.py_ contains the class representing likes on the comments,
as well as functions to manipulate them.
* _postlike.py_ contains the class representing likes on the blog entries,
as well as functions to manipulate them.
* _user.py_ contains the class representing a logged-in user, as well as code
to hash and salt the password.

### HTML templates (/templates)
* _base.html_ is basic HTML code common to all the pages which is rendered by jinja2.
* _mainpage.html_ is the root level page which displays the blog entries.
* _signup.html_ is the form through which users register to interact with the blog.
* _success.html_ welcomes newly signed up users and directs them to main page.
* _login.html_ is the form through which users login.
* _compose.html_ allows users to compose new blog entries.
* _edit.html_ extends _compose.html_ to direct edited entries to the proper URL.

### JavaScript Frontend (/js)
* _main.js_ contains functions called by forms to accept input and make ajax
calls to the backend, updating accordingly without refreshing the page.

### CSS (/stylesheets)
* _main.css_ contains stylings for the page

## Installation
* Install **Google Cloud Platform** following this [guide](https://cloud.google.com/deployment-manager/docs/step-by-step-guide/installation-and-setup).

* To use the local development server, open the Google Cloud SDK Shell.
    * `cd` to the folder where this repository is located.
    * Type `python dev_appserver.py app.yaml` and hit Enter.
        * Note: it may be necessary to include the full path of dev_appserver if
        it is not included in the Python path.  For example:
        `python "C:\Users\user\AppData\Local\Google\Cloud SDK\google-cloud-sdk\platform\google_appengine\dev_appserver.py" app.yaml`
    * The website can be accessed by typing `localhost:8080` into a web browser
    on the local machine.  `localhost:8000` gives access to the site data in the
    Datastore Viewer.

* To publish the site to Google Cloud Platform,
    * Create a [gcloud account](console.cloud.google.com).
    * Create a new project and note the project id.
    * In the Google Cloud SDK Shell, type `gcloud app deploy app.yaml --project [project id]` and
    hit Enter.  Select an appropriate server location, and hit Y to continue.
    * Create indexes by typing `gcloud datastore create-indexes index.yaml --project [project id]`.
    * The website can be accessed at the address [project id].appspot.com.

## License
This project is licensed under the MIT license.
