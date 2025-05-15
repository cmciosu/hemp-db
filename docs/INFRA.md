# HempDB Infrastructure

This page outlines the infrastructure of the HempDB web app and is intended for developers.

## Website

The website is hosted on [Vercel](https://vercel.com). The login for the CMCI Vercel account can be obtained from Dr. Johnny Chen (CMCI). The project uses default configuration for the most part, but specifies `./build.sh` as a custom build step. 

Vercel automatically builds all branches pushed to GitHub. Main branch is configured to be production.

## MySQL Database

The MySQL database used to store all the data for this project is hosted on AWS RDS. The login for the CMCI AWS account can be obtained from Dr. Johnny Chen (CMCI). 

The actual MySQL database has multiple databases within it. Which database you connect to (ex: production or development) can be specified at the end of the connection string after the `/`.