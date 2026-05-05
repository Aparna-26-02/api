from fastapi import APIRouter, HTTPException, Query, Depends
from models.schemas import Student
from routes.dependencies import get_current_user
from data.storage import students
import logging

router = APIRouter()



@router.get("/students")
def get_students(user=Depends(get_current_user)):
    logging.info(f"{user['username']} fetched all students")
    return students



@router.get("/students/{student_id}")
def get_student(student_id: int, user=Depends(get_current_user)):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


@router.post("/students")
def add_student(student: Student, user=Depends(get_current_user)):
    for s in students:
        if s["id"] == student.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    students.append(student.dict())

    logging.info(f"{user['username']} added student {student.id}")

    return {"message": "Student added successfully"}



@router.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student, user=Depends(get_current_user)):
    for index, student in enumerate(students):
        if student["id"] == student_id:
            updated_data = updated_student.dict()
            updated_data["id"] = student_id  # ensure ID consistency

            students[index] = updated_data

            logging.info(f"{user['username']} updated student {student_id}")

            return {"message": "Student updated successfully"}

    raise HTTPException(status_code=404, detail="Student not found")



@router.delete("/students/{student_id}")
def delete_student(student_id: int, user=Depends(get_current_user)):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)

            logging.info(f"{user['username']} deleted student {student_id}")

            return {"message": "Student deleted successfully"}

    raise HTTPException(status_code=404, detail="Student not found")



@router.get("/students/search")
def search_student(name: str = Query(...), user=Depends(get_current_user)):
    result = [
        student for student in students
        if name.lower() in student["name"].lower()
    ]

    if not result:
        raise HTTPException(status_code=404, detail="No students found")

    logging.info(f"{user['username']} searched for '{name}'")

    return result