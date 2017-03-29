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
* _model.py_ contains the entity classes for the data as well as functions to
manipulate that data.
* _entryView.py_ contains the router classes for displaying the main page and
composing, editing, and deleting blog entries.
* _commentView.py_ contains the router classes for displaying and manipulating
comments.
* _likeView.py_ contains the router classes for liking and unliking.
* _loginView.py_ contains the router classes for logging in and out as well as
signing up.
* _handler.py_ contains a class extending the webapp2 handler to simplify
template rendering.
* _utils.py_ contains some necessary helper functions.

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
    * In the Google Cloud SDK Shell, type `gcloud app deploy [project id]` and
    hit Enter.  Select an appropriate server location, and hit Y to continue.
    * Create indexes by typing `gcloud datastore create-indexes index.yaml [project id]`.
    * The website can be accessed at the address [project id].appspot.com.

## License
This project is licensed under the MIT license.
