# GFBio Data Collection Service


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8316119.svg)](https://doi.org/10.5281/zenodo.8316119)


## Description

Collection service is provided by GFBio e.V. and is a central data hub to store and retrieve json for communication and synchronization of user data between different services.

It provides a Rest API for the backends of the connecting Servers to store or retrieve json-data. Each server gets its own secret key for secure retrieval/upload. Therefore the API is required to be accessed from the backends of the using servers.

## Developer Guide

### Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

### Basic Commands

#### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

#### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

##### Running tests with pytest

    $ pytest

#### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

#### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd collection_service
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

#### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

### Deployment

The following details how to deploy this application.

#### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

## Contact Us
Please email any questions and comments to our [Service Helpdesk](mailto:info@gfbio.org) (<info@gfbio.org>).

## Acknowledgements
- This work was supported by the German Research Foundation (DFG) within the project “Establishment of the National Research Data Infrastructure (NFDI)” in the consortium NFDI4Biodiversity (project number [442032008](https://gepris.dfg.de/gepris/projekt/442032008)).
