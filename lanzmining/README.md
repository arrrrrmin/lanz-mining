# lanzmining

Simple python code to parse obsidian vault markdowns.
This code provides a simple flow to produce a final csv file, to visualize or
process the data further.

Fill the `config/example.json` file and point to you'r vault directories.

Run `python src/main.py -c config/example.json` from you'r environment setup, 
to write a `output.csv` file in the `lanzmining` root-dir.

Output columns include:
- index
- episode_name
- date
- description
- talkshow
- factcheck
- length
- name
- role
- message
- party
- media
- group