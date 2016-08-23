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
- .mode columns (make output more readable)

#Roster Scraper#
The roster scraper will populate the database with all the PAC-12 players.  It only needs to be run once before the season starts.  Subsequent runs will add duplicate for each player already in the database.  If the roster needs to be updated, the player table must first be cleared.  Populate the player data with the following commands:
```bash
cd cfbcScraper
./run.sh
```

#Boxscore Scraper#
The boxscore scraper takes a command line argument of gameId. For example:
```bash
cd cfbcScraper
scrapy crawl boxscore -a gameId=<gameId>
```

#Deployment Steps#
```bash
sudo apt-get install git
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo apt-get install libffi-dev
sudo apt-get install libssl-dev 
sudo apt-get install libxml2-dev libxslt1-dev
git clone https://github.com/rmayf/CollegeFootballChallenge.git
cd CollegeFootballChallenge
sudo pip install virtualenv
sudo pip install -r requirements.txt
#Update PrivateSettings.py in cfbc```

