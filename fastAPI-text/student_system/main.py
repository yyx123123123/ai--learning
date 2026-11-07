from fastapi import FastAPI
from . import database
from .schemas import StudentCreate, StudentUpdate

app = FastAPI()
database.create_table()

@app.post("/students")
def insert_student(student: StudentCreate):
    student_id = database.insert_student(student)
    return {"student_id": student_id}

@app.get("/students/all")
def selectall_students():
    students = database.selectall_students()
    return {"students": students}

@app.get("/students/{student_id}")
def selectone_student(student_id: int):
    student = database.selectone_student(student_id)
    if student is None:
        return {"message": "未找到该学生"}
    return {"student": student}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    data = student.model_dump(exclude_unset=True)
    updated_count = database.update_student(student_id, data)
    if updated_count == 0:
        return {"message": "更新失败"}
    return {"message": "更新成功"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    deleted_count = database.delete_student(student_id)
    if deleted_count == 0:
        return {"message": "删除失败"}
    else:
        return {"message": "删除成功"}

