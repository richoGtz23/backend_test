// use backend_test as user and LM5CtcBkAYj93df5 as password to be able to run tests
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username backend_test
python manage.py runserver