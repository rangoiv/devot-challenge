# 🚀 FastAPI + PostgreSQL in Docker

Devot-challenge


## 🛠️ Setup & Run (Docker 🐳)


### 1️⃣ Clone the Repository

### 2️⃣ Create a .env File
Before running the app, create a .env file and add the following variables:

```sh
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql://postgres:mysecretpassword@postgres:5432/mydatabase
```

### 3️⃣ Build & Run with Docker
```sh
sudo docker-compose up --build
```

## 🖥️ Local Development (Without Docker)

Change `DATABASE_URL` to use `localhost` instead of `postgres`.

```sh
python -m venv .venv
source .venv/bin/activat
pip install -r requirements.txt

# Run postgres
sudo docker run -p 5432:5432 --env-file .env -d postgres
export $(cat .env | xargs)
cd app
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📜 Useful Commands

### Stop Local PostgreSQL
```sh
sudo docker stop local-postgres && sudo docker rm local-postgres
```

### Rebuild docker
```sh
sudo docker-compose down --volumes --remove-orphans; sudo docker-compose build; sudo docker-compose up
```