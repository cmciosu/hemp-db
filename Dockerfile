FROM python
WORKDIR /code
EXPOSE 8000
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]