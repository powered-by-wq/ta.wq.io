#!/bin/sh

# Exit on error
set -e

# Dump wq configuration object to file
db/manage.py dump_config --format amd > app/js/data/config.js

# Build javascript with wq.app
cd app;
wq build $1;

# Force important files through any unwanted server caching
cd ../;
sed -i "s/tawq.js/tawq.js?v="$1"/" htdocs-build/tawq.appcache
sed -i "s/tawq.css/tawq.css?v="$1"/" htdocs-build/tawq.appcache

# Preserve Django's static files (e.g. admin)
if [ -d htdocs/static ]; then
    cp -a htdocs/static htdocs-build/static
fi;

# Replace existing htdocs with new version
rm -rf htdocs;
mv -i htdocs-build/ htdocs;

# Restart Django
touch db/tawq/wsgi.py

cd htdocs;
ln -s ../old-static-docs/empty.png ./
ln -s ../old-static-docs/index.html ./
ln -s ../old-static-docs/talks/leaflet-d3-workshop/build/ ./leaflet_d3
ln -s ../old-static-docs/provenance/ ./provenance
ln -s ../old-static-docs/talks/wq-foss4gna/build/ ./wq_foss4g
