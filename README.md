#Setup#
- pip install virtualenv
- pip install -r requirements.txt

###OAUTH Keys###
Cryptography is *hard*.  I'm a bad programmer.  This combination is a security vulnerablitiy waiting to happen.  Let the big dogs run the yard.  In order to utilize Google and Facebook's oauth API, access tokens are required.  Fill out PrivateSettings.py with values supplied by the authentication host.  You can obtain these keys from visiting the sites below:
- [Google] (https://console.developers.google.com/project/dev-aileron-105807/apiui/credential)
- [Facebook] (https://developers.facebook.com/)
- Twitter is currently not supported ( who logs in using twitter anyways? )

Don't forget to comment out NotImplementedError!


#Development#
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver [ip address]:[port]

#Database Access#
- sqlite3 db.sqlite3
