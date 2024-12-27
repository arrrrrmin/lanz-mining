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
goes through the overview page and loads the most recent episodes.

## Initialize database

1. `touch .env` 
2. `pdm run src/lanz_mining/main.py --file <PathToHTMLSource>`

The `.env` file look like:
```bash
DB_HOSTNAME="<DB_HOSTNAME>"
DB_USERNAME="<DB_USERNAME>"
DB_PASSWORD="<DB_PASSWORD>"
DB_NAME="<DB_NAME>"
DB_PORT="<DB_PORT>"
```

In (1) you have to edit this file, like shown above.
(2) will automatically connect to your db and create the tables. From here on,
every call of the `pipeline` either through `main.py` with or without `--file`
argument will write to this database.

## Example exports

A reminder on how to export a `guests.csv` file, from the database to
further work on offline.

```PSQL
\COPY (SELECT lg.lanzepisode_name, lg.name, le.date, lg.role, lg.message FROM lanzguests lg INNER JOIN lanzepisode le ON lg.lanzepisode_name = le.name) TO '<project-path>/lanz-mining/exports/guests.csv' WITH (format csv, header);
```

Transfer the export file to your local directory using `scp` from you'r local 
machine with:

```shell
scp <user>@<server.tld>:<project-dir>/exports/guests.csv ./exports/guests.csv
```

If your want to do manually steps (below), additionally copy the file to 
`./tests/data/guests.csv`, which is the default file for tests to run.


## Steps to do manually

*This project doesn't want to use machine learning or deep learning for data householding*,
so to ensure correct data, there are steps to do manually.
There are helper scripts that find unmapped politicians or journalists without an
associated publication platform, and much more. It's done with a single test file, just
run:

`pdm run helpers`

Details can be found in [tests/dataproc/test_helpers.py](tests/dataproc/test_helpers.py).

```bash
pdm run pytest tests/dataproc/test_helpers.py -s
```

## Exploration

Now that the crawler has looked up data for a while, we can take a look at it and
visualise a few things. Maybe there's something of interest and if not, we found a bit
of transparency for public broadcasting.
