import json
import cv2
import face_recognition
import imutils
import pickle


def load_model(model_file_path='./model_config/model.h5'):
    """
    User-Defined Function, Called whenever we start working with this model
    inputs: model_file_path
    outputs: model loaded object
    """
    data = pickle.loads(open('./model_config/encodings_gilfoyle_hog.pickle', "rb").read())

    return data


def execute_model(frame_data, data):
    """
    User-Defined Function, Called on having frame_data meeting model criteria(1/2/3/.. frame(s))
    inputs: frame_data containing one or more frames as needed by the model specs
    """
    frame = frame_data[0]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame, then compute
    # the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    label = False
    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        label = True in matches
        if(label):
            break
    return label


def load_model_config(model_config_file_path='./model_config/model_config.json'):
    config_map = {}
    with open(model_config_file_path, 'r') as f:
        config_map = json.load(f)

    assert config_map.get('frames_per_exec'), 'frames_per_exec not set'
    assert config_map.get('min_clip_period'), 'min_clip_period not set'
    assert config_map.get('max_clip_period'), 'max_clip_period not set'

    frames_per_exec = config_map.get('frames_per_exec')
    min_clip_period = config_map.get('min_clip_period')
    max_clip_period = config_map.get('max_clip_period')

    model_obj = load_model()

    return frames_per_exec, min_clip_period, max_clip_period, model_obj
