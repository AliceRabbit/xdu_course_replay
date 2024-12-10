import re

def extract_fid_uid_from_cookie(cookie_str):
    # 使用正则表达式从Cookie字符串中提取fid和UID
    fid_match = re.search(r'fid=([^;]+)', cookie_str)
    uid_match = re.search(r'_uid=([^;]+)', cookie_str)
    
    try:
        fid = int(fid_match.group(1)) if fid_match else None
    except ValueError:
        fid = None
    
    try:
        uId = int(uid_match.group(1)) if uid_match else None
    except ValueError:
        uId = None
    
    return {
        'fid': fid,
        'uId': uId
    }