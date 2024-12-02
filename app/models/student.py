from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

class Address(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

    @field_validator('city', 'country', mode='before')
    def validate_non_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError(f"{cls.__name__} cannot be empty or just spaces")
        return value

class Student(BaseModel):
    name: str
    age: int
    address: Address

    @field_validator('name')
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError('Name cannot be empty or just spaces')
        return value

    @field_validator('age')
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError('Age must be a positive integer')
        return value

    @field_validator('address')
    def validate_address(cls, value):
        if not value.city.strip():
            raise ValueError('City cannot be empty or just spaces')
        if not value.country.strip():
            raise ValueError('Country cannot be empty or just spaces')
        return value

    @model_validator(mode='before')
    def check_required_fields(cls, values):
        if 'name' not in values or not values['name'].strip():
            raise ValueError('The "name" field is required and cannot be empty.')
        if 'address' not in values or not values['address']:
            raise ValueError('The "address" field is required.')
        return values

    class Config:
        str_min_length = 1
        str_strip_whitespace = True

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None