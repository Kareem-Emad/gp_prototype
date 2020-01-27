import cv2  # noqa
from model_manager import load_model_config
from video_processor import video_processor


def parse_source(filename, frames_per_exec, model_obj, vid_processor):

    video_buffer = cv2.VideoCapture(filename)
    fps = get_fps(video_buffer)
    total_frames_count = get_frames_count(video_buffer)

    vid_processor.fps = fps

    print(f"Estimated Video Duration: {total_frames_count/fps} seconds")

    frame_buffer = []
    processed_frames_count = 0

    while (video_buffer.isOpened()):
        ret, frame = video_buffer.read()

        print(f'Processing Video {processed_frames_count}/{total_frames_count} frames processed\r', end="")

        if (len(frame_buffer) == frames_per_exec):
            vid_processor.process_frames(frame_buffer, model_obj)
            vid_processor.flush_to_indexer()

            frame_buffer = []
        else:
            frame_buffer.append(frame)

        processed_frames_count += 1

    video_buffer.release()


def get_fps(video_buffer):
    fps = round(video_buffer.get(cv2.CAP_PROP_FPS))
    print(f"Frames per second: {fps}")
    return fps


def get_frames_count(video_buffer):
    frame_count = int(video_buffer.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Frames per second: {frame_count}")
    return frame_count


frames_per_exec, min_clip_period, max_clip_period, model_obj = load_model_config()
vid_processor = video_processor(min_clip_period, max_clip_period, frames_per_exec)

parse_source('Friends_s3Ep01.mp4', frames_per_exec, model_obj, vid_processor) # noqa
