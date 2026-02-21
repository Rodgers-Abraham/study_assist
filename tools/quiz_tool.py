import json
import re 
from langchain_core.tools import tool 

@tool
def generate_quiz(notes_content: str) -> str:
    """
   -  Generate 5 multi-choice questions based on notes
    - Return a JSON string of questions options and correct 
    answer
    input: the lecture note or summary 
    """
    
    return f""" 
   Generate exactly 5 multi choice quiz questions from this content:
   {notes_content}
   Return only valid JSON array with this exact structure (no markdown, no extra text)
   [
       {{
           "question" : "//Question text/// here?//",
           "options" : {{
               "A" : "//OptionA//",
               "B" : "OptionB",
               "C" : "OptionC",
               "D" : "OtionD"
           }},
           "answer" : "A",
           "topic" : "short topic label"
       }}
   ]
"""

def parse_quiz_json(raw: str) -> list:
    """
    extract and parse the JSON quiz array as an LLM output 
    """
    #cleaned json
    cleaned = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()
    
    # find the new json array 
    start = cleaned.find("[")
    end = cleaned.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError("NO JSON ARRAY FOUND IN QUIZ RESPONSE")
    
    return json.loads(cleaned[start:end])
    