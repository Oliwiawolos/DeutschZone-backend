<<<<<<< HEAD
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
=======
FROM python:3.11 
WORKDIR /app 
COPY . .
RUN pip install --no-cache-dir -r requirements.txt 
EXPOSE 5000
CMD ["python", "app.py"] 
>>>>>>> 4c4017b5518e81d32f652941314f84cfc82df308
