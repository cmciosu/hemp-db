# Build Pipeline

### This document contains information on the build pipeline for HempDB. This documentation is intended for developers.

## Github Actions

The github actions are run on every PR opened to main, as well as every push to main. They need to pass for a PR to be merge-able. 

For the checks to pass, the code must be linted, all migrations must run successfully, and the [test suite](https://github.com/cmciosu/hemp-db/blob/main/helloworld/tests.py) must run

## Vercel

Vercel runs [build.sh](https://github.com/cmciosu/hemp-db/blob/main/build.sh) for the build step. For this to pass, just make sure all dependencies are listed in [requirements.txt](https://github.com/cmciosu/hemp-db/blob/main/requirements.txt) and all versions are correct.
