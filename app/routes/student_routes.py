from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Response, status
from models.student import Student, StudentUpdate
from services.student_service import (
    create_student_service,
    list_students_service,
    get_student_service,
    update_student_service,
    delete_student_service,
)
from bson import ObjectId

router = APIRouter()

@router.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    try:
        response = create_student_service(student.model_dump())
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error while creating student"
        )

@router.get("/students")
async def list_students(
    country: Optional[str] = Query(None, description="Filter students by country"),
    age: Optional[int] = Query(None, description="Filter students by minimum age (inclusive)")
):
    try:
        students = list_students_service(country=country, age=age)
        return {"data": students}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error while filtering students"
        )

@router.get("/students/{student_id}")
async def fetch_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid student ID format"
        )
    student = get_student_service(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.patch("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_id: str, student_update: StudentUpdate):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid student ID format"
        )
    update_data = student_update.model_dump(exclude_unset=True)
    updated_student = update_student_service(student_id, update_data)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: str):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid student ID format"
        )
    success = delete_student_service(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return Response(status_code=status.HTTP_200_OK)