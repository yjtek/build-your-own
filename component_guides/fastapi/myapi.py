from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel, Field

# uvicorn myapi:app --reload
app = FastAPI()


class Student(BaseModel):
    name: str = Field(default='')
    age: int = Field(default=-1)
    year: str = Field(default='')
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

students: dict[int, Student|UpdateStudent] = {
    1: Student(name='john', age=17, year='year 12'),
    2: Student(name='johanna', age=18, year='year 13'),
    3: Student(name='steve', age=99, year='year 100'),
}

@app.get('/')
def index():
    return {'name': 'first data'}

@app.get('/get-student/{student_id}')
def get_student(student_id: int = Path(description='ID of the student you want', gt=0, lt=3)) -> UpdateStudent | Student | None:
    return students.get(student_id, None)

@app.get('/get-by-name')
def get_student_by_name(name: Optional[str] = None):
    if name is None:
        return students
    return_students = {}
    
    for student in students:
        compare_name = students.get(student, Student()).name
        if compare_name:
            if name in compare_name:
                return_students[student] = students.get(student)

    return return_students

@app.get('/get-by-name/{student_id}')
def get_student_by_name_combine_path_and_query_param(student_id: int, name: Optional[str] = None):
    if name is None:
        return students
    return_students = {}
    for student in students:
        compare_name = students.get(student, Student()).name
        if compare_name:
            if name in compare_name:
                return_students[student] = students.get(student)
    
    return_students[99] = Student(name=str(student_id))

    return return_students

@app.post('/create-student/{student-id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    
    students[student_id] = student
    return students[student_id]

@app.put('/update-student/{student-id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {'Error': 'Student does not exist'}
    
    students[student_id] = Student()

    if student.name:
        students[student_id].name = student.name

    if student.age:
        students[student_id].age = student.age

    if student.year:
        students[student_id].year = student.year

    return students[student_id]
    
@app.delete('/delete-student/{student-id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {'error': 'student does not exist'}
    
    del students[student_id]
    return {'Succes': f'{student_id=} deleted'}

    