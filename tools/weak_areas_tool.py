import json
import os
from datetime import datetime
from langchain_core.tools import tool

WEAK_AREAS_FILE = os.path.join(os.path.dirname(__file__), "..", "data",
                               "weak_areas.json")


def _load_weak_areas() -> list:
    if not os.path.exists(WEAK_AREAS_FILE):
        return []
    with open(WEAK_AREAS_FILE, "r") as f:
        return json.load(f)


def _save_weak_areas(data: list):
    os.makedirs(os.path.dirname(WEAK_AREAS_FILE), exist_ok=True)
    with open(WEAK_AREAS_FILE, "w") as f:
        json.dump(data, f, indent=2)
        
@tool
def save_weak_area(topic: str, question: str, user_answer: str, 
                   correct_answer: str) ->  str:
    """
    save a weak area when the student answers wrongly in the quiz 
    Inputs : parameters
    """
    weak_areas = _load_weak_areas()
    
    #check if the topic exists in my json
    existing = next((w for w in weak_areas if w["topic"] == topic), None)
    
    # create weak area if not existing 
    entry = {
        "question" : question,
        "user_answer" : user_answer,
        "correct_answer" : correct_answer,
        "timestamp" : datetime.now().isoformat
    }
    if existing:
        existing['count'] = existing.get("count", 1) + 1
        existing['mistakes'].append(entry)
    else:
        weak_areas.append({
            "topic" : topic, 
            "count" : 1,
            "mistakes" : [entry]
        })
    _save_weak_areas(weak_areas)
    return f" weak area saved under this topic: {topic}"