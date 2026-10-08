from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from redactor import sanitize_prompt, rehydrate_response

app = FastAPI(title="LLM Privacy Protection Gateway")

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"

@app.post("/v1/chat/secure-generate")
async def secure_generate(request: ChatRequest):
    sanitized_prompt, session_vault = sanitize_prompt(request.prompt)
    
    try:
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', 'MOCK_KEY')}"}
        payload = {
            "model": request.model,
            "messages": [{"role": "user", "content": sanitized_prompt}]
        }
        
        cloud_completion = f"I have processed the query for {sanitized_prompt}."

        final_output = rehydrate_response(cloud_completion, session_vault)
        
        return {
            "status": "success",
            "sanitized_sent": sanitized_prompt,
            "response": final_output
        }
        
    finally:
        session_vault.clear()
