from fastapi import FastAPI
from routes.student_routes import router as student_router

app = FastAPI()

app.include_router(student_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Management App!"}