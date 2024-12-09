import requests
import yaml
from urllib.parse import unquote, urlparse, parse_qs
import json

def load_config(file_path):
    """
    读取配置文件。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"配置文件 {file_path} 未找到。")
    except yaml.YAMLError as e:
        print(f"加载配置文件时出错: {e}")
    return None

def fetch_videopage_url(url, headers, data):
    """
    发送 GET 请求获取视频页面。
    """
    try:
        response = requests.get(url, headers=headers, params=data)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return None
    

def get_videopage_url(course_id):
    """
    获取视频页面实际地址。
    """
    config = load_config("config.yaml")
    if config is None:
        return
    url = "http://newesxidian.chaoxing.com/live/getViewUrlHls"
    headers = config.get("headers")
    params = {
        "liveId": course_id,
        "status": 2,
        "jie": None,
        "isStudent": None
    }
    videopage_url = fetch_videopage_url(url, headers, params)
    videopage_url = unquote(videopage_url)
    return videopage_url

def fetch_videoplayer(course_id):
    """
    获取独立的视频播放器 (双播放器页面)。
    """
    config = load_config("config.yaml")
    if config is None:
        return
    videopage_url = get_videopage_url(course_id)
    headers = config.get("headers")
    params = {
        "liveId": course_id,
        "status": 2,
        "jie": None,
        "isStudent": None
    }
    try:
        response = requests.get(videopage_url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return
    print(response.content)

def get_video_urls(course_id):
    """
    获取真实视频地址。
    """
    videopage_url = get_videopage_url(course_id)
    parsed_url = urlparse(videopage_url)
    query_params = parse_qs(parsed_url.query)
    info_json_str = query_params.get('info', [''])[0]
    info_dict = json.loads(info_json_str)
    ppt_video_url = info_dict['videoPath']['pptVideo']
    teacher_track_url = info_dict['videoPath']['teacherTrack']
    urls = {
        "ppt_video": ppt_video_url,
        "teacher_track": teacher_track_url
    }
    return urls
