```
$ pip install -r requirements.txt
$ createdb colors
$ cp config/settings.example.py config/settings.py
```
and edit appropriately.

Populate the db
```python
from scripts import db
db.init_db()
db.populate_db()
db.populate_colors_in_db()
```

To run app locally:

```
$ fab run
```
