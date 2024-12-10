import requests
from utils.config import load_config
from utils.id__helpers import extract_fid_uid_from_cookie
import re


def fetch_course_data(url, headers, data):
    """
    发送 POST 请求获取课程数据。
    """
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None


def parse_course_data(course_data):
    """
    解析课程数据，提取关键信息。
    """
    return [
        {
            "courseName": item.get("courseName", "未知课程"),
            "days": item.get("days", "未知周次"),
            "weekDay": item.get("weekDay", "未知星期"),
            "jie": item.get("jie", "未知节次"),
            "teacherRealName": item.get("teacherRealName", "未知教师"),
            "id": item.get("id", "未知ID"),
            "status": item.get("status", "-1"),
        }
        for item in course_data
    ]


def display_course_data(courses):
    """
    打印课程信息，仅用于调试。
    """
    for course in courses:
        print(f"课程名称: {course['courseName']}")
        print(f"第{course['days']}周")
        print(f"周{course['weekDay']}")
        print(f"第{course['jie']}节")
        print(f"教师名称: {course['teacherRealName']}")
        print(f"视频 ID: {course['id']}")
        print(f"状态: {course['status']}")
        print("-" * 40)


def get_courses_list(liveId):
    # 配置请求参数
    config = load_config("config.yaml")
    if config is None:
        return
    url = "http://newesxidian.chaoxing.com/live/listSignleCourse"
    headers = config.get("headers")
    data = extract_fid_uid_from_cookie(headers['Cookie'])
    data['liveId'] = liveId

    # 获取课程数据
    raw_data = fetch_course_data(url, headers, data)
    courses = []

    if raw_data:
        # 解析并展示课程数据
        courses = parse_course_data(raw_data)
    return courses