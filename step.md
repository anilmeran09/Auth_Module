Alembic migrations (Windows PowerShell)

1) Activate virtualenv
```powershell
./venv/Scripts/Activate.ps1
```

2) Set required env vars (this project reads `DATABASE_URL` and `ENVIRONMENT`)
```powershell
$env:DATABASE_URL = "postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME"
$env:ENVIRONMENT = "development"
```

3) Create a new migration from model changes
```powershell
alembic revision --autogenerate -m "Describe your change"
```

4) Apply migrations
```powershell
alembic upgrade head
```

Useful commands
```powershell
alembic current            # show current DB revision
alembic history --verbose  # show migration history
alembic show heads         # show head revisions
alembic downgrade -1       # revert last migration
alembic downgrade base     # revert to base
alembic stamp head         # mark DB as up-to-date without running scripts
```

Notes
   - Run commands from the project root (same folder as `alembic.ini`).
   - Make sure your models in `core/models.py` reflect desired schema before autogenerate.
   - If `DATABASE_URL` is missing, the app will raise an error (see `core/config.py`).

---