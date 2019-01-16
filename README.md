```
$ pip install -r requirements.txt
$ createdb colors
``` 

Populate the db
```python
from scripts import db
db.init_db()
db.populate_db()
```

To run app locally:

```
$ fab run
```