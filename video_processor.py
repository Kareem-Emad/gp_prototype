import json
import time
from model_manager import execute_model
from video_indexer import video_indexer


class video_processor:
    def __init__(self, min_clip_period, max_clip_period, frames_per_exec):
        self.tags_seq = []
        self.fps = 0
        self.min_clip_period = min_clip_period
        self.max_clip_period = max_clip_period
        self.frames_per_exec = frames_per_exec
        self.num_flushed = 0
        self.vid_indexer = video_indexer()
        self.indexed_data = self.read_stored_indexed_clips('./index_database.json')

    def read_stored_indexed_clips(self, file_path):
        try:
            with open(file_path, 'r') as f:
                json_str = f.read()
                json_data = json.loads(json_str)
                return json_data
        except Exception:
            return {'data': []}
        return {'data': []}

    def process_frames(self, frame_buffer, model_obj):
        tag = execute_model(frame_buffer, model_obj)
        self.tags_seq.append(tag)

    def needs_flush(self):
        return len(self.tags_seq) * self.frames_per_exec >= self.max_clip_period * self.fps

    def flush_to_indexer(self):
        if(self.needs_flush()):
            clips = self.vid_indexer.extract_clips(self.tags_seq)
            self.flush_to_disk(clips)
            self.tags_seq = []
            self.num_flushed += 1

    def flush_to_disk(self, clips):
        starting_frame_index = self.max_clip_period * self.fps * self.num_flushed

        for clip in clips:
            start_period_frame, end_period_frame = clip

            start_period_frame, end_period_frame = start_period_frame + starting_frame_index, end_period_frame + starting_frame_index
            start_period_second, end_period_second = int(start_period_frame / self.fps), int(end_period_frame / self.fps)

            start_period_second = time.strftime('%H:%M:%S', time.gmtime(start_period_second))
            end_period_second = time.strftime('%H:%M:%S', time.gmtime(end_period_second))

            print(f"Interest Period between  {start_period_second} and {end_period_second} in video")
            self.indexed_data['data'].append({'start_at': start_period_second, 'end_at': end_period_second})

        try:
            with open('./index_database.json', 'w') as f:
                f.write(json.dumps(self.indexed_data))
        except Exception:
            print("Failed To write updated index to database, will retry next flush isa")
