FROM python:2.7

COPY . /usr/share/app
RUN pip install --no-cache-dir -r /usr/share/app/requirements.txt

ENTRYPOINT ["python", "/usr/share/app/docker-entrypoint.py"]
