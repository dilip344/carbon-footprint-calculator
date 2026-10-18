from pydantic import BaseModel,Field
class RegisterInput(BaseModel):
 name:str=Field(min_length=2,max_length=120); email:str=Field(min_length=5,max_length=160); password:str=Field(min_length=6,max_length=100)
class LoginInput(BaseModel): email:str; password:str
class AuthResponse(BaseModel): user_id:int; name:str; email:str
