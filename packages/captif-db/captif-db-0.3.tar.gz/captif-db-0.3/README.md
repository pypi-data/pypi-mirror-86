
# captif-db

Object relational mapping for the CAPTIF database.

These are low-level methods.

### Initialise database and generate a session object:

```
import captif_db
captif_db.DbSession.global_init()
session = captif_db.DbSession.factory()
```

### Import and use models:

```
from captif_db.models import Project
projects = session.query(Project).all()
```
