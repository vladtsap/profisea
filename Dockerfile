FROM python:3

EXPOSE 5000

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV FLASK_ENV development
ENV FLASK_APP app.py
CMD ["flask", "run", "-h", "0.0.0.0"]