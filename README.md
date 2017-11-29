Follow steps to setup flask environment

1. Install flask through pip
2. mkdir web
3. cd to web
4. Create virtual environment for flask (not neccesary but recommended)
	$ python -m venv flask
5. Run the following code lines for installing neccesary flask librabries
	$ flask\Scripts\pip install flask
	$ flask\Scripts\pip install flask-login
	$ flask\Scripts\pip install flask-openid
	$ flask\Scripts\pip install flask-mail
	$ flask\Scripts\pip install flask-sqlalchemy
	$ flask\Scripts\pip install sqlalchemy-migrate
	$ flask\Scripts\pip install flask-whooshalchemy
	$ flask\Scripts\pip install flask-wtf
	$ flask\Scripts\pip install flask-babel
	$ flask\Scripts\pip install guess_language
	$ flask\Scripts\pip install flipflop
	$ flask\Scripts\pip install coverage
6. Create a basic structure of the application
	$ mkdir app
	$ mkdir app/static
	$ mkdir app/templates
	$ mkdir tmp
7. Make sure to install any packages you require for your development if you are using virtual environment. I have used following packages and have thus installed in my virtual environment.
	flask\Scripts\pip install pandas
	flask\Scripts\pip install twitter
	flask\Scripts\pip install textblob
	flask\Scripts\pip install plotly
	flask\Scripts\pip install markupsafe
	flask\Scripts\pip install us
