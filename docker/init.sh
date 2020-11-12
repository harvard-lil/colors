#!/bin/bash

docker-compose up -d

# make sure the database server is ready
sleep 5

docker-compose exec db createdb colors --user postgres

# the last step here takes about thirteen minutes on
# a 3.1 GHz quad-core Intel Core i7
docker-compose exec web python -c "\
from scripts import db ;\
db.init_db() ;\
db.populate_db() ;\
db.populate_colors_in_db()"
