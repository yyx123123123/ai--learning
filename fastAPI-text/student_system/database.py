from pathlib import Path
import sqlite3
from .schemas import StudentCreate, StudentUpdate

DB_PATH = Path(__file__).resolve().parent / "student.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    conn = connect_db()
    conn.execute("""
    create table if not exists student (id integer primary key autoincrement,
    password integer,
    name text,
    age integer,
    datetime text )
    """)
    conn.commit()
    conn.close()
    return "创建表成功"

def insert_student(student: StudentCreate):
    conn = connect_db()
    cursor = conn.cursor()
    from datetime import datetime
    cursor.execute("""
    insert into student (password, name, age, datetime)
    values (?, ?, ?, ?)
    """, (student.password, student.name, student.age, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return student_id

def selectall_students():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    select * from student
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def selectone_student(student_id: int):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    select * from student where id=?
    """, (student_id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return None
    conn.close()
    return dict(row)

def update_student(student_id: int, data: dict):
    conn = connect_db()
    cursor = conn.cursor()
    fields = []
    values = []
    for key, value in data.items():
        if value is not None:
            fields.append(f"{key}=?")
            values.append(value)
    values.append(student_id)
    if not fields:
        conn.close()
        return 0
    cursor.execute(f"""
    update student set {', '.join(fields)} where id=?
    """, values)
    conn.commit()
    updated_count = cursor.rowcount
    conn.close()
    return updated_count


def delete_student(student_id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    delete from student where id=?
    """, (student_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count
