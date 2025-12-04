from pydantic import BaseModel, Field
from typing import List, Literal

Level = Literal["School", "HighSchool", "Bachelors", "Masters"]
Language = Literal["English", "Nepali", "Hindi"]

class TimeWindow(BaseModel):
    dow: Literal["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start: str  # "HH:MM"
    end: str    # "HH:MM"

class CoursePref(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    priority: int = Field(ge=1, le=10)

class StudentOnboarding(BaseModel):
    level: Level
    courses: List[CoursePref] = Field(min_length=1)
    min_budget: int = Field(ge=0, le=200000)
    max_budget: int = Field(ge=0, le=200000)
    language: Language
    preferred_time: List[TimeWindow] = Field(min_length=1)
