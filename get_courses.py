import requests
from utils.config import load_config
import json
import datetime

def fetch_courses():
    config = load_config("config.json")
    if config is None:
        return
    headers = config.get("headers")
    fid = config.get("fid")
    userId = config.get("uId")
    termYear = datetime.datetime.now().year
    termId = get_current_termId()
    week = 4
    url = f"https://newesxidian.chaoxing.com/frontLive/listStudentCourseLivePage?fid={fid}&userId={userId}&week={week}&termYear={termYear}&termId={termId}&type=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # 格式化输出 JSON 数据
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)

def get_current_termId():
    month = datetime.datetime.now().month

    if 3 <= month <= 8:
        return 2
    else:
        return 1

def main():
    fetch_courses()

if __name__ == "__main__":
    main()