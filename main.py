from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from HuggingfaceLLM import generate_text

app = FastAPI()

# Correct the origin, remove the trailing slash
origins = ["http://localhost:3000"]

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from this frontend origin
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)

# Define request model
class ChatRequest(BaseModel):   
    message: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate/")
async def generate_text_api(chat_request: ChatRequest):
    response = generate_text("google/gemma-2-2b-it", chat_request.message)
    return response

# Run the server with the following command: uvicorn main:app --reload
