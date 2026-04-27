from fastapi import FastAPI
from routes import auth, students
from middleware.logger import log_time

app = FastAPI()

app.middleware("http")(log_time)

app.include_router(auth.router)
app.include_router(students.router)

@app.get("/")
def home():
    return {"message": "FastAPI Practice Project"}