FROM python:3.12.1-slim

WORKDIR /app

COPY catalog.py .
COPY catalog.txt .

RUN pip install flask requests

EXPOSE 5001

CMD ["python", "catalog.py"]
