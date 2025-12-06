from fastapi import FastAPI, HTTPException
from app.models import StudentOnboarding
from app.storage import save_preferences, get_preferences
from app.tutors import TUTORS
from app.recommender import recommend
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="TutorLinker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# For now, we use a fixed logged-in user id (mock)
MOCK_USER_ID = 2

@app.get("/")
def root():
    return {"message": "TutorLinker backend is running"}

@app.post("/student/onboarding")
def student_onboarding(payload: StudentOnboarding):
    # basic sanity: max should be >= min
    if payload.max_budget < payload.min_budget:
        raise HTTPException(status_code=400, detail="max_budget must be >= min_budget")

    save_preferences(MOCK_USER_ID, payload.model_dump())
    return {"saved": True, "user_id": MOCK_USER_ID}

@app.get("/student/preferences")
def student_preferences():
    prefs = get_preferences(MOCK_USER_ID)
    if not prefs:
        raise HTTPException(status_code=404, detail="No preferences found. Complete onboarding first.")
    return prefs

@app.get("/student/recommendations")
def student_recommendations():
    prefs = get_preferences(MOCK_USER_ID)
    if not prefs:
        raise HTTPException(status_code=404, detail="No preferences found. Complete onboarding first.")

    ranked = recommend(prefs, TUTORS)
    return ranked[:10]
