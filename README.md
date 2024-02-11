# lanz-mining

A repo for collecting data about the german talk show *Markus Lanz*.
As a public tv station we find awefully less information and statics
about the selective process of guest invitation and topic selection.
So this repository aims to record some hands on statistics about this
largely popular tv format, watched by many german languaged people.

## How to collect data

There are two main ways to collect the data. Both find the data on
the official zdf media library. Either (1) search for "*Markus Lanz*"
on the official page [zdf.de](https://www.zdf.de) and load as many 
episodes as possible and save the source html. You can then use
`pdm run src/lanz_mining/main.py --file <PathToHTMLSource>` to 
download the metadata from every episode listed in this search 
result page. Or (2) regularly trigger the main-page crawler which
goes through the overview page and loads the most recent 6 episodes.

## Init environment

The `.env` file look like so:
```bash
DB_HOSTNAME="<DB_HOSTNAME>"
DB_USERNAME="<DB_USERNAME>"
DB_PASSWORD="<DB_PASSWORD>"
DB_NAME="<DB_NAME>"
DB_PORT="<DB_PORT>"
```

## Initialize database

1. `touch .env` 
2. `pdm run src/lanz_mining/main.py --file <PathToHTMLSource>`

In (1) you have to edit this file, [like shown above](#init-environment).
(2) will automatically connect to your db and create the tables. From here on,
every call of the `pipeline` either through `main.py` with or without `--file`
argument will write to this database.


## Example exports

A reminder on how to export a `guests.csv` file, from the database to
further work on offline.

```PSQL
\copy
(SELECT lg.lanzepisode_name, lg.name, le.date, lg.role, lg.message 
FROM lanzguests lg 
INNER JOIN lanzepisode le ON lg.lanzepisode_name = le.name) 
to '/Users/arminmuller/Devel/lanz-mining/database_exports/guests.csv' with (format csv, header);
```