from fastapi import FastAPI

app = FastAPI(title="TutorLinker API")

@app.get("/")
def root():
    return {"message": "TutorLinker backend is running"}
