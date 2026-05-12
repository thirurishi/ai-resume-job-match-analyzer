from fastapi import FastAPI

app = FastAPI(title="AI Resume & Job Match Analyzer API")

@app.get("/")
async def root():
    return {"message": "AI Resume & Job Match Analyzer API is running"}