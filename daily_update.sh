#!/bin/sh

clear
echo "\n======================================
RUNNING ALL DAILY UPDATES:
====================================="

# ============================== GENERAL CRAWLING ==============================
#Run crawl modules
# echo "\n=======================
# Crawling Guardian site:
# ======================="
# python guardian_main_crawl.py

# echo "\n=======================
# Wrangling Guardian data:
# ======================="
# python guardian_main_wrangle.py

# Can run the following for any date range
# and with any tag filter at any time.
# Will only pull articles not already dealt with.
# echo "\n=======================
# Crawling Facebook data:
# ======================="
# python facebook_crawl.py

# echo "\n=======================
# Wrangling Facebook data:
# ======================="
# python facebook_wrangle.py

# Can run the following for any date range
# and with any tag filter at any time.
# Will only pull articles not already dealt with.
# Can take a while...
# echo "\n=======================
# Crawling Guardian link data:
# ======================="
# python guardian_link_crawl.py

# echo "\n=======================
# Wrangling Guardian link data:
# ======================="
# python guardian_link_wrangle.py

# ============================== 2D GRID CALCULATIONS ==============================
# Run algorithms
# TF-IDF takes a long time...
# echo "\n=======================
# Calculating TF-IDF scores:
# ======================="
# python tf_idf_scikit.py

# Create output
# echo "\n=======================
# Creating HTML grid output:
# ======================="
# python grid.py


# ============================== BUTTERFLY EFFECT CALCS ==============================
# Calculate cosine similarities and kmean clustering and save to python module
# Note we run in incremental mode, though can be run in 'fresh' mode too to recalculate
# See file for details (or just run python ../flask/butterfly_main.py fresh)
echo "\n=======================
Calculating data for Butterfly Effect visualisation:
======================="
python ../flask/butterfly_main.py incremental



# ============================== PUSH TO GIT/HEROKU ==============================

# echo "\n=======================
# Git add/commit/push to Github and Heroku:
# ======================="
# git add .
# git commit -m "Automatic daily update"
# git push origin master
# git push heroku master

# echo "\n=======================
# Finished - exiting.
# ======================="