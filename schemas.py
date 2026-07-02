from pydantic import BaseModel

#input Schema 
class BlogCreate(BaseModel):
    title: str
    content: str

#Output Schema
class BlogResponse(BaseModel):
    id : int
    title : str
    content : str

    class config:
        from_attributes = True