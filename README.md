In order to run locally, you must have Postgres set up, and you should
set up a virtual environment, however you normally do so, or something like

```
python3 -m venv env
source env/bin/activate
```

Then run

```
pip install -r requirements.txt
pip install torch==0.4.1.post2
createdb colors
cp data/color_results_copy.txt data/color_results.txt
cp config/settings.example.py config/settings.py
```

and edit appropriately.

Populate the db

```python
from scripts import db
db.init_db()
db.populate_db()
db.populate_colors_in_db()
```

and run the app:

```
$ fab run
```

Alternatively, you can use `docker-compose`; this takes care of the
database and the virtual environment for you:

```
cp config/settings.example.py config/settings.py
cp data/color_results_copy.txt data/color_results.txt
bash ./docker/init.sh
docker-compose exec web fab run
```

In both cases, the step of `db.populate_colors_in_db()` is
time-consuming, presently about thirteen minutes on a 3.1 GHz
quad-core Intel Core i7.
