from typing import List, Dict

# Dummy tutors (later this will come from your database)
TUTORS: List[Dict] = [
    {
        "tutor_id": 1,
        "name": "Ramesh Koirala",
        "levels": ["HighSchool", "Bachelors"],
        "courses": ["Maths", "Physics"],
        "languages": ["English", "Nepali"],
        "hourly_rate": 1200,
        "rating_avg": 4.7,
        "rating_count": 26,
        "availability": [
            {"dow": "Tue", "start": "18:00", "end": "20:00"},
            {"dow": "Thu", "start": "18:00", "end": "20:00"}
        ],
        "verified": True
    },
    {
        "tutor_id": 2,
        "name": "Anita Thapa",
        "levels": ["School", "HighSchool"],
        "courses": ["English", "IELTS"],
        "languages": ["English"],
        "hourly_rate": 1500,
        "rating_avg": 4.8,
        "rating_count": 31,
        "availability": [
            {"dow": "Mon", "start": "19:00", "end": "21:00"},
            {"dow": "Thu", "start": "18:00", "end": "20:00"}
        ],
        "verified": True
    },
    {
        "tutor_id": 3,
        "name": "Prakash Lama",
        "levels": ["HighSchool"],
        "courses": ["Chemistry", "Biology"],
        "languages": ["English", "Nepali"],
        "hourly_rate": 1800,
        "rating_avg": 4.5,
        "rating_count": 19,
        "availability": [
            {"dow": "Tue", "start": "18:00", "end": "19:30"},
            {"dow": "Sat", "start": "14:00", "end": "16:00"}
        ],
        "verified": True
    },
    {
        "tutor_id": 4,
        "name": "Mina KC",
        "levels": ["School"],
        "courses": ["Maths", "Science", "English"],
        "languages": ["Nepali", "English"],
        "hourly_rate": 900,
        "rating_avg": 4.2,
        "rating_count": 11,
        "availability": [
            {"dow": "Wed", "start": "16:00", "end": "18:00"},
            {"dow": "Fri", "start": "16:00", "end": "18:00"}
        ],
        "verified": True
    },
    {
        "tutor_id": 5,
        "name": "Sunil Mishra",
        "levels": ["Bachelors", "Masters"],
        "courses": ["Data Engineering", "DBMS", "Python"],
        "languages": ["English", "Hindi"],
        "hourly_rate": 2000,
        "rating_avg": 4.9,
        "rating_count": 40,
        "availability": [
            {"dow": "Tue", "start": "18:00", "end": "20:00"},
            {"dow": "Thu", "start": "19:00", "end": "21:00"}
        ],
        "verified": True
    },
    {
        "tutor_id": 6,
        "name": "Unverified Tutor",
        "levels": ["HighSchool"],
        "courses": ["Maths"],
        "languages": ["English"],
        "hourly_rate": 1000,
        "rating_avg": 4.6,
        "rating_count": 10,
        "availability": [{"dow": "Tue", "start": "18:00", "end": "20:00"}],
        "verified": False
    }
]
