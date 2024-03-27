
# Setup local database
- Install PostgreSQL (https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) and select following options in installer wizard:
  - PostgreSQL Server
  - Command Line Tools
  - pgAdmin 4 (optional - useful UI to inspect data)
  - set superuser and password to `postgres`
- Add bin directory to PATH environment variable (e.g. C:\Program Files\PostgreSQL\16\bin)
- In PowerShell: 
  - run `psql -U postgres`
  - enter superuser password `postgres`
  - run `CREATE DATABASE quant-lifters;`
  - run `exit`
- The database is ready, once `python manage.py migrate` and `python manage.py createsuperuser` are executed as part of backend setup.

# Setup backend
- Install [Python 3.12](https://www.python.org/downloads/)
- Clone this repo and open the folder in your IDE (I use VS Code)
- In repo root, run `pip install -r requirements.txt`
- Set the following environment variables:
  - QUANT_LIFTERS_UI_URL: http://localhost:3000
  - QUANT_LIFTERS_DJANGO_SECRET_KEY: Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- In repo root, run `python manage.py createsuperuser` and fill required data.
- run `python manage.py migrate`. Also run this after pulling changes of the data model (i.e. new migration files).

# Run the backend locally
- In repo root, run `python manage.py runserver` (or start with VS code run and debug)
- Visit http://127.0.0.1:8000/admin/ and enter your superuser credentials

# Copy prod data into local db
In PowerShell (passwords need to be properly set before - works out-of-the box if pgAdmin is connected to prod db): 
  - run `psql -U postgres`
  - enter superuser password `postgres`
  - run `pg_dump -C -h [remote host address] -U quant_lifters_read_only_user quant_lifters | psql -h localhost -U postgres quant_lifters`
  - run `exit`
