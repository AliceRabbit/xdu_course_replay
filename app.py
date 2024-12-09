from flask import Flask, render_template, request
from course_list import get_courses_list
from video_capturer import get_video_urls

app = Flask(__name__)

@app.route('/')
def index():
    courses = get_courses_list()
    return render_template('index.html', courses=courses)

@app.route('/play')
def play():
    course_id = request.args.get('course_id')
    if not course_id:
        return "Invalid course ID", 400
    
    params = {
        'courseName': request.args.get('courseName'),
        'days': request.args.get('days'),
        'weekDay': request.args.get('weekDay'),
        'jie': request.args.get('jie'),
        'teacherRealName': request.args.get('teacherRealName')
    }
    
    try:
        video_urls = get_video_urls(course_id)
    except Exception as e:
        return f"Error fetching video URLs: {str(e)}", 500
    
    return render_template('replay_player.html', video_urls=video_urls, **params)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)