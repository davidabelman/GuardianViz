README
=======

Project to visualise news in interesting ways. This repo contains the backend functionality for pulling data from the Guardian, from Facebook, compiling all data into correct data structures, daily script to run, etc.

The Flask app itself is stored in a separate repo (https://github.com/davidabelman/GuardianVizFlask)

Notes
-----
To change which article set is being analysed, see options.current_articles_path. This should be set to 'all' for the main analysis.

To print status on articles collected, see general_functions.print_current_status(). This will print number of articles collected, and so on.

To run the daily script, run:
>> sh daily_update.sh

It looks in options.py for date range for crawl (crawl_start_datetime, crawl_end_datetime). You should set these dates manually in the file. It then pulls Guardian data, Guardian link data, and Facebook data for these dates. It carries out calculations etc for 2D grid and butterfly effect, and uploads to Heroku.

Possible to run any of the following commands individually (these are what make up the daily update). Note that all data between stages is saved in the directory '/data' (which is not loaded to the git repo). Once again, date parameters must be altered within the 'options.py' file.

Pulling the guardian article data and saving to disk (requests according to date only, so duplicates may be pulled if run twice with same date ranges)

>> python guardian_main_crawl.py
>> python guardian_main_wrangle.py

Pulling Facebook data on any guardian articles pulled (not revisited if pulled previously, even if within date range)

>> python facebook_crawl.py
>> python facebook_wrangle.py

Pulling internal links between Guardian articles (not revisited if pulled previously, even if within date range)

>> python guardian_link_crawl.py
>> python guardian_link_wrangle.py

Performing '2D grid visualisation' calculations and saving json output

>> python tf_idf_scikit.py
>> python grid.py

Performing 'Butterfly Effect' visualisation (incremental signifies only additional articles are added to the cosine similarity calculations, rather than starting from afresh)

>> python ../flask/butterfly_main.py incremental