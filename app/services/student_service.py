from typing import Optional
from db.queries import insert_student, get_students_with_filters, get_student_by_id, update_student, delete_student
from bson import ObjectId
from fastapi import HTTPException

def create_student_service(student_data: dict) -> dict:
    student_id = insert_student(student_data)
    return {"id": student_id}

from db.queries import get_students_with_filters

def list_students_service(country: Optional[str] = None, age: Optional[int] = None) -> list:
    return get_students_with_filters(country=country, age=age)


def get_student_service(student_id: str) -> dict:
    student = get_student_by_id(student_id)
    if student:
        return student
    else:
        return None

def update_student_service(student_id: str, update_data: dict) -> dict:
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    updated_student = update_student(student_id, update_data)
    if updated_student:
        updated_student["_id"] = str(updated_student["_id"])
        return updated_student
    else:
        raise HTTPException(status_code=400, detail="Failed to update student")

def delete_student_service(student_id: str) -> dict:
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    success = delete_student(student_id)
    if success:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to delete student")
