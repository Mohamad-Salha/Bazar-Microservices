FROM python:3.12.1-slim

WORKDIR /app

COPY order.py .

ENV CATALOG_URL=http://catalog:5001

RUN pip install flask requests

EXPOSE 5002

CMD ["python", "order.py"]
