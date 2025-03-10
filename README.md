# Setting up the Backend

### Create a .env file:
```bash
cp .env.example .env
```

### Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate # Linux/Mac
venv/Scripts/activate # Windows
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Set up the database:
```bash
alembic init alembic
```

### Create the database:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Run the application:
```bash
uvicorn app.main:app --reload
```