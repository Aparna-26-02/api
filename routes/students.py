from fastapi import APIRouter, HTTPException, Query, Depends
from models.schemas import Student
from utils.security import verify_token
from data.storage import students
import logging

router = APIRouter()


@router.get("/students")
def get_students(user=Depends(verify_token)):
    logging.info(f"{user['sub']} fetched all students")
    return students


@router.get("/students/{student_id}")
def get_student(student_id: int, user=Depends(verify_token)):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


@router.post("/students")
def add_student(student: Student, user=Depends(verify_token)):
    for s in students:
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    students.append(student.dict())
    logging.info(f"{user['sub']} added student {student.id}")
    return {"message": "Student added"}


@router.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student, user=Depends(verify_token)):
    for index, student in enumerate(students):
        if student["id"] == student_id:
            students[index] = updated_student.dict()
            logging.info(f"{user['sub']} updated student {student_id}")
            return {"message": "Student updated"}

    raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/students/{student_id}")
def delete_student(student_id: int, user=Depends(verify_token)):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            logging.info(f"{user['sub']} deleted student {student_id}")
            return {"message": "Student deleted"}

    raise HTTPException(status_code=404, detail="Student not found")


@router.get("/search")
def search_student(name: str = Query(...), user=Depends(verify_token)):
    result = [
        student for student in students
        if name.lower() in student["name"].lower()
    ]

    if not result:
        raise HTTPException(status_code=404, detail="No students found")

    logging.info(f"{user['sub']} searched for {name}")
    return result