# GPN23-LanzMining

A repository with all resources for my CFP submission to GPN23, Hidden Patterns. 

## Get data

Since scraping is increasingly disliked and excluded from the most terms of use, 
I recommend a less _automated_ process. Another aspect is the new ZDF-Webstreaming
application, which requires to be familiar with _selenium_ or other 
webdriver-frameworks.

I'd recommend using [Obsidian Web Clipper](https://obsidian.md/clipper) together 
with an AI providers API endpoint. You can also host you'r own open source model
and use you'r own endpoints.

You can use my [configs](configs/) and customize for you'r own vault.

### Install

* Install [`python3.12.*`](https://www.python.org/downloads/release/python-31210/) on you'r computer
* Either install [lanzmining](lanzmining/) with [pdm](https://pdm-project.org/latest/), [poetry](https://python-poetry.org) or directly from [requirements.txt]

### Process data

To finally obtain you'r dataset you can use the [lanzmining](lanzmining/) 
processors like so: `python src/main.py -c config/vault.json`

## Vis data

All visualizations for the talk are build with d3js, so I decided to wrap it in a
svelte project. If you'r not familiar with it, all vis code is build in simple js.
You can find it at [visuals/src/lib/visualisations](visuals/src/lib/visualisations).

The data itself lives at [visuals/static/data](visuals/static/data).

