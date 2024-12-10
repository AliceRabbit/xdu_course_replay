import requests
from utils.config import load_config
from utils.id__helpers import extract_fid_uid_from_cookie
import json
import datetime
import os
import time
def fetch_courses(week):
    """
    获取单周课表。
    """
    config = load_config("config.yaml")
    if config is None:
        return
    headers = config.get("headers")
    cookies = headers['Cookie']
    fid_uid = extract_fid_uid_from_cookie(cookies)
    fid = fid_uid.get("fid")
    userId = fid_uid.get("uId")
    termYear = datetime.datetime.now().year
    termId = get_current_termId()
    url = f"https://newesxidian.chaoxing.com/frontLive/listStudentCourseLivePage?fid={fid}&userId={userId}&week={week}&termYear={termYear}&termId={termId}"
    print(url)
    response = requests.get(url, headers=headers)
    data = response.json()
    
    return data

def get_current_termId():
    """
    获取估算的学期ID。
    """
    month = datetime.datetime.now().month

    if 3 <= month <= 8:
        return 2
    else:
        return 1

def fetch_all_courses_data():
    """
    获取所有课程及其首个courseId和liveId，并持久化到文件，避免重复请求。
    """
    courses_data = {}
    if os.path.exists("courses.json"):
        with open("courses.json", "r", encoding="utf-8") as f:
            try:
                courses_data = json.load(f)
                if not is_valid_courses_data(courses_data):
                    raise ValueError("Invalid data format")
            except (json.JSONDecodeError, ValueError):
                courses_data = {}
    
    if not courses_data:
        for week in range(1, 18):
            current_week_courses = fetch_courses(week)
            for course in current_week_courses:
                courseName = course.get("courseName")
                courseId = course.get("courseId")
                liveId = course.get("id")
                if courseName not in courses_data:
                    courses_data[courseName] = {
                        "courseId": courseId,
                        "liveId": liveId
                    }
            time.sleep(0.5)
        with open("courses.json", "w", encoding="utf-8") as f:
            json.dump(courses_data, f, ensure_ascii=False)
    return courses_data

def is_valid_courses_data(data):
    """
    检查持久化的课程数据是否有效。
    格式: {"courseName": {"courseId": id, "liveId": id}}
    """
    if not isinstance(data, dict):
        return False
    for course_name, course_info in data.items():
        if not isinstance(course_name, str):
            return False
        if not isinstance(course_info, dict):
            return False
        if not all(key in course_info for key in ("courseId", "liveId")):
            return False
        if not isinstance(course_info["courseId"], int) or not isinstance(course_info["liveId"], int):
            return False
    return True