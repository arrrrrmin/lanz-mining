# Lanz Mining

Free data on guests, topics, parties and experts on the german ZDF talk show 
*Markus Lanz*. Public data from the ZDF media organisation that belongs to all 
citizens.

## What's it about?

Is a **work-in-progress** project to crawl data from the german talk show
*Markus Lanz*. This project aims to free up some data that is part of
germany's public service media media landscape. Open data approaches 
should be a standard for every public service. 
Open data and transparency also helps the credibility of public service media 
as a whole.  

## Requires

* Python3.11
* Postgres installed for development
* (Optional) Node installed

## Installation

* Fork and clone the repo
* Install the python dependencies with you'r favourite package management tools 
* Create your postgres database
* Run `touch .env` and fill the entries for you'r database (see below)
* Run `pdm run src/lanz_mining/main.py` to crawl actual pages not existing in your db

The `.env` file look like:
```bash
DB_HOSTNAME="<DB_HOSTNAME>"
DB_USERNAME="<DB_USERNAME>"
DB_PASSWORD="<DB_PASSWORD>"
DB_NAME="<DB_NAME>"
DB_PORT="<DB_PORT>"
```

Ok, now deploy it on you'r server or instance and run it through a cron-job and 
get new data as soon as it appears.

## Work with aquired data

To work further with the data, we need to export and copy things to our repository.
Export it like so:
```PSQL
\COPY (SELECT lg.lanzepisode_name, lg.name, le.date, lg.role, lg.message FROM lanzguests lg INNER JOIN lanzepisode le ON lg.lanzepisode_name = le.name) TO '<project-path>/lanz-mining/exports/guests.csv' WITH (format csv, header);
```
And transfer it to your repo like so:
```shell
scp <user>@<server.tld>:<project-dir>/exports/guests.csv exports/guests.csv
cp exports/guests.csv tests/data/guests.csv
```

If you now want to process the data and find genres, party associations or 
media platforms of journalists, run `pdm run process`. 
For more details on what this does see `src/lanz_mining/process.py`.
You can also skip this and explore the data directly with some example plots
with `pdm run explore`. This writes a few plots to `figures/`. 

### Check data quality

To ensure correct data, there are steps to do manually.
There are helper scripts that find unmapped politicians or journalists without an
associated publication platform, and much more. It's done with a few tests, 
just run: `pdm run helpers`. The tests step through a few categories and show
uncovered mappings for genres, politicians or media outlets.

### More data

Simply running the crawler for a while will take ages to get a reasonable 
amount of data, so there's a little solution for this. Open your browser
go to the official [zdf.de](https://www.zdf.de) page and search for "*Markus Lanz*".
Load as many episodes as possible and save the source html. You can then use
`pdm run src/lanz_mining/main.py --file <PathToHTMLSource>` to 
download the data from every episode listed in this search result page.

# Contributions

Currently I'm looking to reduce the manual tasks more, so idealy everything runs
automatically. To get this reliable, I'd be thankful for any hints on public 
APIs or other methods to map genres, identify party memberships and alike.
Further I'd really be happy if you let me know what you think, DM me on 
[chaos.social/@arrrrrmin](https://chaos.social/@arrrrrmin), or open an issue to
further improve things.
