# HempDB Infrastructure

### This Document outlines the infrastructure of the HempDB web app. This document is intended for developers.

## Website

The website is hosted on [Vercel](https://vercel.com). The login for the CMCI Vercel account can be obtained from Dr. Johnny Chen (CMCI). The project uses default configuration for the most part, but specifies ./build.sh as a custom build step. 

Vercel automatically builds all branches pushed to github. Main branch is configured to be production.

## CI

We use Github Actions for CI. The only action used can be found in the [.github directory](/.github/workflows/migrate-test-lint.yml). It simply runs the test suite, migrations, and lints. This happens only on **opened pull requests to main** and **pushes to main**. 

## MySQL Database

The MySQL database used to store all the data for this project is hosted on AWS RDS. The login for the CMCI AWS account can be obtained from Dr. Johnny Chen (CMCI). 