# Tasklish

> BY: Safal Neupane
> Started on: 22 May 2023

Tasklish is a productivity app for minimalists. My idea of Tasklish is, people would use this to plan their life, holidays, treakking, and
study. Professionals would love this, as this allows, integreated payment processing, calendar management, personalized link to allow booking
appointments, and a custom landing page for businesses and hobbies alike.

## Installation
*Install `make` which will make the whole process smoooth.*

### Using `Make`

1. The `Makefile` relies on `PROJECT_NAME` environment variable, so Let's export it:
```bash
export PROJECT_NAME=tasklish-django
```

2. Make environment variable.
```bash
# We're using venv
make venv
```

3. Use the `alias` command as shown by `Make`'s output. It will make your life easier.
```bash
alias activate=source ~/.pyvenv/tasklish-django/bin/activate

activate
```

4. Time to setup Django project.
```bash
# This will do the `pip install` command.
make install
```

5. Do the database migration.
```bash
make migrate
```

6. Run the local server.
```bash
make run
```

### Without using `Make`

1. Setup a virtual environment. We're using `venv`
```bash
# I like to organise my virtual environments in one place: ~/.pyvenvs
python3 -m venv ~/.pyvenvs/tasklish-django

# Activate the venv
source ~/.pyvenvs/tasklish-django/bin/activate

# Or, set the alias so, you can use `activate` to simply activate the venv
alias activate="source ~/.pyvenvs/tasklish-django/bin/activate"

activate
```

2. Setup Django.
```bash
python -m pip install --upgrade pip

python pip install -r dev.requirements.txt
```

3. Database migrate
```bash
python manage.py migrate
```

4. Run server
```bash
python manage.py runserver
```


## API Docs

After you run the local server, head over to `localhost:8000/api-docs/`. This includes the API docs generated using `drf_yasg`.
