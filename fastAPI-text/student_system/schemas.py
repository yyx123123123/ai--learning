from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    password: int = Field(..., description="密码")
    name: str = Field(..., description="姓名")
    age: int=Field(...,ge=18, description="年龄")

class StudentUpdate(BaseModel):
    password: int|None=None
    name: str|None=None
    age: int|None=None


