# File Structure

### This document outlines the file structure used for the HempDB project. This document is intended for developers / maintainers. 

## ~/hempdb

Contains Django configuration files [settings.py](/hempdb/settings.py) and top-level urls [urls.py](/hempdb/urls.py) (auth URLs, homepage)

## ~/helloworld

Contains the main Django application. Most of the logic is implemented in this folder. 
- [urls.py](/helloworld/urls.py) contains all model routes, as well as routes to misc. pages. 
- [views.py](/helloworld/views.py) contains all the View logic for all helloworld routes.
- [models.py](/helloworld/models.py) contains our schema
- [forms.py](/helloworld/forms.py) contains all model forms
### /helloworld/templates

All the template files used across the site. The registration subdirectory holds all template files related to auth

## ~/.github

Hosts Github Actions

## ~/docs

Hosts documentation
