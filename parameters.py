
from typing import Dict, List
from AnimationStates.animation import Animation, AParameters
import numpy as np

from tha3.poser.modes.pose_parameters import get_pose_parameters


pose_parameter_count = 0
for pose_parameter in get_pose_parameters().get_pose_parameter_groups():
    pose_parameter_count += pose_parameter.get_arity()

class AParametersTha(AParameters):
    """
    Talking Head Anime

    Animation Parameters
    """
    pose_parameters = get_pose_parameters()
    pose_parameter_groups = get_pose_parameters().get_pose_parameter_groups()
    pose_parameter_count = pose_parameter_count

    def __init__(self, array: np.ndarray | dict[str, float] | list[float] | None = None):
        if array is None:
            array = np.array([0.0] * AParametersTha.pose_parameter_count)
        elif isinstance(array, np.ndarray):
            self.array = array
        elif isinstance(array, list):
            array = np.array(array)
        elif isinstance(array, dict):
            self.__init__()
            for k, v in array.items():
                self[k] = v
        else:
            raise NotImplementedError()
    
    def get_parameter_index(self, pose_parameter_name):
        return AParametersTha.pose_parameters.get_parameter_index(pose_parameter_name)
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.array[key] = value
        elif isinstance(key, str):
            self.array[self.get_parameter_index(key)] = value
        else:
            raise KeyError(f'Invalid key type {type(key)}')

    def __add__(self, other: 'AParametersTha') -> AParameters:
        return AParametersTha(self.array + other.array)

    def __radd__(self, other: 'AParametersTha') -> AParameters:
        return AParametersTha(other.array + self.array)

    def __mul__(self, scalar: float) -> AParameters:
        return AParametersTha(self.array * scalar)
    
    def __rmul__(self, scalar: float) -> AParameters:
        return AParametersTha(self.array * scalar)

    @classmethod
    def from_list(cls, param_list: List[Dict[str, float]|List[float]]):
        """
        Animation_tha.states_from_list([
            {'eyebrow_happy_left': 1.0},
            {'eyebrow_happy_right': 1.0},
        ])
        """
        s_list = []
        if len(param_list) == 0:
            return s_list
        if (isinstance(param_list[0], dict) or
            isinstance(param_list[0], list) or
            isinstance(param_list[0], np.ndarray)
        ):
            for s in param_list:
                s_list.append(AParametersTha(s))
        else: 
            raise NotImplementedError()
        return s_list


def model_input_split(model_input_arr, time_counter):
    return {
        "eyebrow_vector_c": model_input_arr.array[:12],
        "mouth_eye_vector_c": model_input_arr.array[12:12+27],
        "pose_vector_c": model_input_arr.array[12+27:12+27+6],
        "time_counter": time_counter,
    }