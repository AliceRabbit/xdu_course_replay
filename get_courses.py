import requests
from utils.config import load_config
import json
import datetime
import os
def fetch_courses(week):
    config = load_config("config.yaml")
    if config is None:
        return
    headers = config.get("headers")
    fid = config.get("data").get("fid")
    userId = config.get("data").get("uId")
    termYear = datetime.datetime.now().year
    termId = get_current_termId()
    url = f"https://newesxidian.chaoxing.com/frontLive/listStudentCourseLivePage?fid={fid}&userId={userId}&week={week}&termYear={termYear}&termId={termId}"
    print(url)
    response = requests.get(url, headers=headers)
    data = response.json()
    
    return data

def get_current_termId():
    month = datetime.datetime.now().month

    if 3 <= month <= 8:
        return 2
    else:
        return 1

def fetch_all_coursesId():
    coursesId = {}
    if os.path.exists("courses.json"):
        with open("courses.json", "r", encoding="utf-8") as f:
            try:
                coursesId = json.load(f)
                if not is_valid_courses_data(coursesId):
                    raise ValueError("Invalid data format")
            except (json.JSONDecodeError, ValueError):
                coursesId = {}
    
    if not coursesId:
        for week in range(1, 18):
            current_week_courses = fetch_courses(week)
            for course in current_week_courses:
                courseName = course.get("courseName")
                courseId = course.get("courseId")
                coursesId.setdefault(courseName, courseId)
        with open("courses.json", "w", encoding="utf-8") as f:
            json.dump(coursesId, f, ensure_ascii=False)
    
    print(coursesId)
    return coursesId

def is_valid_courses_data(data):
    if not isinstance(data, dict):
        return False
    for key, value in data.items():
        if not isinstance(key, str) or not isinstance(value, int):
            return False
    return True
def main():
    fetch_all_coursesId()

if __name__ == "__main__":
    main()