import json
import numpy as np


def load_model(model_file_path='./model_config/model.h5'):
    """
    User-Defined Function, Called whenever we start working with this model
    inputs: model_file_path
    outputs: model loaded object
    """
    pass


def execute_model(frame_data, model):
    """
    User-Defined Function, Called on having frame_data meeting model criteria(1/2/3/.. frame(s))
    inputs: frame_data containing one or more frames as needed by the model specs
    """
    if(model):
        return np.random.randint(2)
    else:
        return np.random.randint(2)


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
