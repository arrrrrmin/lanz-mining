# Lanz Mining

## What's it about?

Crawl talkshow guests, descriptions, political party memberships and all other 
available information from ARD and ZDF public media's web presence.
Crawlers and parsers support *Markus Lanz*, *Maischberger*, *Maybrit Illner*,
*Caren Miosga* and *Hart aber fair*. Public media data should be publically 
available (public money, public data).

## Requires

* Python3.11
* Postgres installed for development
* (Optional) Node installed

## Installation

* Fork and clone the repo
* Install the python dependencies with you'r favourite package management tools
* (Optionally) use [pdm](https://pdm-project.org/latest/).

## Crawl and extract data

### Crawling commands

To get the data locally run `pdm run python -m src.lanz_mining.crawl -t <targetShow>`.
This project currently supports following `targetShows`:
* `markuslanz`, `maybritillner`, `carenmiosga`, `maischberger`, `hartaberfair`
* If you'r using it with a cronjob, use `--lates-only`-flag.

There's another option for ZDF-`targetShow`s. Visit [zdf-mediathek](https://www.zdf.de), 
find the search field and enter the name of you'r `targetShow` and hit the checkbox
for 'ganze Sendungen' and load as many results as possible. Next save the html page and
run `pdm run python -m src.lanz_mining.crawl -t <targetShow> --file <htmlFile>`.

Any of the combinations above will write found html files to `outputs/html`. 

This will visit all urls found in the file and saves all episodes html files.

### Extract data

When you got some html files ready, you need to run
`pdm run python -m src.lanz_mining.scrape_local --input-dir outputs/html --output-file data-processed.csv`.

Information extraction is done with regexes to match certain indicators on e.g. roles.
In cases where information is missing, `scrape_local` tries to find information in other
formats using the guests name.

# Contributions

Currently I'm looking to reduce the manual tasks more, so idealy everything runs
automatically. To get this reliable, I'd be thankful for any hints on public 
APIs or other methods to map genres, identify party memberships and alike.
Further I'd really be happy if you let me know what you think, DM me on 
[chaos.social/@arrrrrmin](https://chaos.social/@arrrrrmin), or open an issue to
further improve things.
