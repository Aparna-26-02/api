from fastapi import FastAPI,HTTPException,Query,Request,Header
from pydantic import BaseModel
import time
import logging
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
app=FastAPI()

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'

)

@app.middleware('http')
async def log_time(request: Request, call_next):
    start = time.time()
    logging.info(f"Request Started: {request.method} {request.url}")

    response = await call_next(request)
    process_time = time.time() - start
    logging.info(f"Request Time: {process_time: 4f} sec")
    return response

def verify_token(token: str):
    if token != SECRET_TOKEN:
       logging.warning("Unauthorized acces attempt")
       raise HTTPException(status_code=401, detail = 'Unauthorized')
class Student(BaseModel):
    id: int
    name: str
    course: str

class Login(BaseModel):
    username: str
    password: str


students = []

@app.get('/')
def home():
    logging.info("home api called")
    return {'message': 'FastAPI Practice Project'}

@app.get("/students")
def get_students(token: str = Header(...)):
    verify_token(token)
    logging.info("fetch all students")
    return students

@app.get("/students/{student_id}")
def get_student(student_id : int, token: str = Header(...)):
    verify_token(token)
    for student in students:
        if student['id'] == student_id:
            logging.info(f"Fetch student id {student_id}")
            return student
    logging.error("student not found")    
    raise HTTPException(status_code=404, detail='Student not found')
    
@app.post("/login")
def login(user: Login):
    if user.username == ADMIN_USERNAME and user.password == ADMIN_PASSWORD:
        logging.info("login success")
        return {"token": SECRET_TOKEN}
    logging.error("login failed")
    raise HTTPException(status_code=401,detail = 'invalid username or password')
@app.post('/students')
def add_student(student: Student, token: str = Header(...)):
    verify_token(token)
    students.append(student.dict())
    logging.info(f"Added student{student.name}")
    return {'message':"student added"}

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student,token: str = Header(...)):
    verify_token(token)
    for index, student in enumerate(students):
        if student['id'] == student_id:
            students[index] = updated_student.dict()
            logging.info(f"updated student id {student_id}")
            return {"message" : "student updated"}
    logging.error("Update failed : student not found")    
    raise HTTPException(status_code=404, detail='Student not found')
    
@app.delete("/students/{student_id}")
def delete_student(student_id: int, token: str = Header(...)):
    verify_token(token)
    for student in students:
        if student['id'] == student_id:
            students.remove(student)
            logging.info(f"deleted student id{student_id}")
            return{'message':"student deleted"}
    logging.error("Delete failed : student not found")    
    raise HTTPException(status_code=404, detail='Student not found')

@app.get('/search')
def  search_student(name: str = Query(...), token: str = Header(...)):
    verify_token(token)
    result = [student for student in students if student['name'].lower()== name.lower()]
    logging.info(f"Searched student{name}")
    return result      

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  
    
    
