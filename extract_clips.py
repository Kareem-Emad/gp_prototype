import getpass
import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

username = getpass.getuser()


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


file_path = './index_database.json'
json_data = {}
try:
    with open(file_path, 'r') as f:
        json_str = f.read()
        json_data = json.loads(json_str)
except Exception:
    print(f'Fuck you, {username}. feen el data :v?!')


try:
    clip_id = 0
    for clip in json_data['data']:
        start_second = get_sec(clip['start_at'])
        end_second = get_sec(clip['end_at'])

        ffmpeg_extract_subclip("mm.mp4", start_second, end_second, targetname=f"./clips/clip_{clip_id}.mp4")
        clip_id += 1
except KeyError:
    print('malformed data')
