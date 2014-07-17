#!/bin/sh

clear
echo "\n======================================
RUNNING ALL DAILY UPDATES:
====================================="

# Run crawl modules
echo "\n=======================
Crawling Guardian site:
======================="
python guardian_main_crawl.py

echo "\n=======================
Wrangling Guardian data:
======================="
python guardian_main_wrangle.py

echo "\n=======================
Crawling Facebook data:
======================="
python facebook_crawl.py

echo "\n=======================
Wrangling Facebook data:
======================="
python facebook_wrangle.py

echo "\n=======================
Crawling Guardian link data:
======================="
python guardian_link_crawl.py

echo "\n=======================
Wrangling Guardian link data:
======================="
python guardian_link_wrangle.py

# Run algorithms
# TF-IDF takes a long time...
# echo "\n=======================
# Calculating TF-IDF scores:
# ======================="
# python tf_idf_scikit.py

# Create output
echo "\n=======================
Creating HTML grid output:
======================="
python grid.py

echo "\n=======================
Finished - exiting.
======================="