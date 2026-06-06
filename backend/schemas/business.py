from pydantic import BaseModel

class BusinessCreate(BaseModel):
   name: str
   owner: str
   email: str
