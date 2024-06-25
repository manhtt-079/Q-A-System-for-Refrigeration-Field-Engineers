from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    

if __name__ == "__main__":
    pass