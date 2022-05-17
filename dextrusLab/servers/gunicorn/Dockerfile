FROM python
RUN pip install gunicorn
WORKDIR /app
COPY app.py .
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]