FROM python:3.10-slim

# Update the package manager and install security updates
RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["uvicorn", "app.main:src", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "main.py"]