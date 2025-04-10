# Build Pipeline

### This document contains information on the build pipeline for HempDB. This documentation is intended for developers.

## Github Actions

The github actions are run on every PR opened to main, as well as every push to main. They need to pass for a PR to be merge-able. 

For the checks to pass, the code must be linted, all migrations must run successfully, and the [test suite](https://github.com/cmciosu/hemp-db/blob/main/helloworld/tests.py) must run

## Vercel

Vercel runs [build.sh](https://github.com/cmciosu/hemp-db/blob/main/build.sh) for the build step. For this to pass, just make sure all dependencies are listed in [requirements.txt](https://github.com/cmciosu/hemp-db/blob/main/requirements.txt) and all versions are correct.

* Recent (Spring 2025) changes to the Django CI file `.github/workflows/migrate-test-lint.yml`:
    - `python manage.py migrate helloworld --fake-initial || python manage.py migrate helloworld --noinput`: intended to resolve common CI test deployment issues defensively. https://docs.djangoproject.com/en/5.2/topics/migrations/

        - `python manage.py migrate helloworld --fake-initial`: attempts to test the migration for a deployment assuming that initial migration changes have already been applied in the past. Necessary for first-time deployments when building the database from a backup or if it is initialized in another way.
        - `python manage.py migrate helloworld --noinput`: guarantees an attempt to migrate to the database from the start. Useful for resolving conflicts arising from missing migration files or inconsistent database schemas that may be ahead of other git branches.