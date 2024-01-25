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
