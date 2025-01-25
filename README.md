# fastapireact

fastapi + react + auth0

## Configurar alembic

```
from src.models import Base
from src.database import DATABASE_URL

# Configurar metadata, por defecto es None
target_metadata = Base.metadata

# Configurar conexión a la base de datos
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```
