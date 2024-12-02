from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Response, status
from models.student import Student, StudentUpdate
from services.student_service import create_student_service, list_students_service, get_student_service, update_student_service, delete_student_service

router = APIRouter()

@router.post("/students", status_code=status.HTTP_201_CREATED)
async def create_students(student: Student):
    student_data = student.model_dump(exclude_unset=True)
    response = create_student_service(student_data)
    return response

@router.get("/students")
async def list_students(
    country: Optional[str] = Query(None, description="Filter students by country"),
    age: Optional[int] = Query(None, description="Filter students by minimum age (inclusive)")
):
    students = list_students_service(country=country, age=age)
    return {"data": students}

@router.get("/students/{id}")
async def fetch_student(student_id: str):
    student = get_student_service(student_id)
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@router.patch("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_id: str, student_update: StudentUpdate):
    update_data = student_update.model_dump(exclude_unset=True)
    
    updated_student = update_student_service(student_id, update_data)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: str):
    success_message = delete_student_service(student_id)
    return Response(status_code=status.HTTP_200_OK)