import os
from typing import Optional
from pymongo.collection import Collection
from bson import ObjectId
from db.connection import client

# DB_NAME = os.environ.get("DB_NAME")
DB_NAME = "db1"

database = client[DB_NAME]
students_collection: Collection = database["students"]

def insert_student(student_data: dict) -> str:
    result = students_collection.insert_one(student_data)
    return str(result.inserted_id)

def get_students_with_filters(country: Optional[str] = None, age: Optional[int] = None) -> list:
    query = {}

    if country:
        query["address.country"] = country

    if age is not None:
        query["age"] = {"$gte": age}

    students = list(students_collection.find(query, {"_id": 0}))

    return students

def get_student_by_id(student_id: str) -> dict:
    try:
        student = students_collection.find_one({"_id": ObjectId(student_id)}, {"_id": 0})
        if student:
            return student
        return None
    except Exception as e:
        return None


def update_student(student_id: str, update_data: dict) -> dict:
    try:
        existing_student = students_collection.find_one({"_id": ObjectId(student_id)})

        if not existing_student:
            return None

        if "address" in update_data:
            update_data["address"] = {
                **existing_student.get("address", {}),
                **update_data["address"],
            }

        updated_student = students_collection.find_one_and_update(
            {"_id": ObjectId(student_id)},
            {"$set": update_data},
            return_document=True
        )

        return updated_student
    except Exception as e:
        print(f"Error updating student: {e}")
        return None


def delete_student(student_id: str) -> bool:
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count > 0