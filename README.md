# Project Name

## Project Setup
This project can be used as a Django template. To use it:
```bash
django-admin startproject --template https://github.com/howieweiner/howies-django-template --extension=py,md --name=Makefile
```

## Getting Started

Create a virtual environment and install the requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt
```

Ensure Docker is running and start the database and redis containers,
from a separate terminal window:

```bash
docker-compose up
```

Create a `.env` file in the root of the project with the following values:

```bash
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1
DATABASE_URL=psql://postgres:postgres@localhost:5432/postgres
NEW_USER_PASSWORD=changeme
EMAIL_FROM_ADDRESS=hello@builtbyhowie.co.uk
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_PORT=1025
SENDGRID_API_KEY=XYZ
SITE_ADDRESS=http://localhost:8000
```

Create a Django superuser:

```bash
make createsuperuser
```

Start the development server:

```bash
make serve
```

Compiling Tailwind CSS:
If you are adding any Tailwind css classes, then you will need to recompile the css file.
A watcher task can run in the background to do this:

```bash 
make tailwind
```

## Docs

- [Server Setup](docs/server_setup.md)
- [Infrastructure setup for DigitalOcean](docs/infra.md)
- [Deployment](docs/deployment.md)
