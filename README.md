# Initial setup
- Install [VS Code](https://code.visualstudio.com/download)
- Install [Python 3.12](https://www.python.org/downloads/)
- Clone this repo and open the folder in VS code
- In repo root, run `pip install -r requirements.txt`
- Set the following environment variables:
  - QUANT_LIFTERS_POSTGRE_PASSWORD: `ask Pierre`
  - QUANT_LIFTERS_POSTGRE_URL: dpg-cmvsehvqd2ns73cf0u40-a.frankfurt-postgres.render.com
  - QUANT_LIFTERS_UI_URL: http://localhost:3000
  - QUANT_LIFTERS_DJANGO_SECRET_KEY: `Generate one with python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- In repo root, run `python manage.py createsuperuser` and fill required data.

*This setup will connect your local backend to the remote database. I'll add instructions on how to run the DB locally.*
  
# Run the backend locally
- In repo root, run `python manage.py runserver`
- Visit http://127.0.0.1:8000/admin/ and enter your superuser credentials
