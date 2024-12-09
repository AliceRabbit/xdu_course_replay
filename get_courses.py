import requests
from utils.config import load_config
import json

def fetch_courses():
    url = "https://newesxidian.chaoxing.com/frontLive/listStudentCourseLivePage?fid=16820&userId=323992114&week=3&termYear=2024&termId=1&type=1"
    headers = load_config("config.yaml").get("headers")
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # 格式化输出 JSON 数据
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)

def main():
    fetch_courses()

if __name__ == "__main__":
    main()