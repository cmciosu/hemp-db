import pymysql

"""
This file is needed for the MySQL connection to properly work
mysqlclient does not work on vercel, so we had to use pymysql instead

for reference: https://stackoverflow.com/questions/76041512/error-while-installing-mysqlclient-on-vercel-for-django-app
"""
pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()