** INSTALATION GUIDE

1. Create your mysql database with a name such as 'baseballstats'

2. Copy the source code to a folder such as 'C:\SportScraper'

3. Using phpMyAdmin (or other mysql tool) to import this sql file C:\SportScraper\sql\script.sql into the above database

4. Update the database setting DATABASE_CONNECTION_STRING in the setting file C:\SportScraper\BaseBallStats\settings.py with your database username and password. Here is the format DATABASE_CONNECTION_STRING = 'mysql+mysqldb://<username>:<password>@localhost/<database>'
E.g. if username is 'root', password is 'admin123' and database name 'baseballstats', we will have below setting value
DATABASE_CONNECTION_STRING = 'mysql+mysqldb://root:admin123@localhost/baseballstats'

5. (optional) You can update your proxy list at C:\SportScraper\proxy.txt

6. (optional) Install correct version for Firefox (https://www.mozilla.org) and GeckoDriver using this link https://github.com/mozilla/geckodriver/releases/

For current version
- GeckoDriver: https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-win64.zip

Extracting the GeckoDriver zip file to C:\SportScraper\geckodriver.exe

Extracting the GeckoDriver zip file to C:\SportScraper\geckodriver.exe
Then update GECKODRIVER_PATH in the setting file to the full path of geckodriver.exe
E.g. GECKODRIVER_PATH = 'C:\SportScraper\geckodriver.exe'

7. Install python at https://www.python.org/downloads/ (tested in version 3.9.1 at https://www.python.org/downloads/release/python-391/)
and all modules defined in C:\SportScraper\requirements.txt

8. Open command line and go to the folder C:\SportScraper, type this command line to run: scrapy crawl sport_scraper --nolog

9. All scraped data will be inserted into 2 corressponding tables: hitting and pitching. If there is any error, it will be log IP and game url into table blocking_ips_game

10. That's all