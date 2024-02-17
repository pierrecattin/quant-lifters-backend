# Initial setup
- Install [Python 3.12](https://www.python.org/downloads/)
- Clone this repo and open the folder in your IDE (I use VS Code)
- In repo root, run `pip install -r requirements.txt`
- Set the following environment variables:
  - QUANT_LIFTERS_UI_URL: http://localhost:3000
  - QUANT_LIFTERS_DJANGO_SECRET_KEY: Generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- In repo root, run `python manage.py createsuperuser` and fill required data.
- run `python manage.py makemigrations trainer; python manage.py migrate`. Also rerun this if you change the data model.

# Run the backend locally
- In repo root, run `python manage.py runserver` (or start with VS code run and debug)
- Visit http://127.0.0.1:8000/admin/ and enter your superuser credentials
