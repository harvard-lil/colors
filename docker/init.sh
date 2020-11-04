#!/bin/bash

docker-compose up -d

sleep 5

docker-compose exec db createdb colors --user postgres

# this is a bad workaround for inability to specify this version
# in requirements.in
docker-compose exec web pip install torch==0.4.1.post2

# the last step here takes quite a lot of time
docker-compose exec web python -c "\
from scripts import db ;\
db.init_db() ;\
db.populate_db() ;\
db.populate_colors_in_db()"
