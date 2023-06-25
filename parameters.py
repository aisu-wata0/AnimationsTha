
from typing import Dict, List
from dataclasses import dataclass, field
from AnimationStates.animation import Animation, AParameters
import numpy as np

from tha3.poser.modes.pose_parameters import get_pose_parameters


parameter_count = 0
for pose_parameter in get_pose_parameters().get_pose_parameter_groups():
    parameter_count += pose_parameter.get_arity()

@dataclass
class AParametersTha(AParameters):
    """
    Talking Head Anime

    Animation Parameters
    """
    parameter_count = parameter_count
    pose_parameters = get_pose_parameters()
    pose_parameter_groups = get_pose_parameters().get_pose_parameter_groups()

    def __init__(self, array: np.ndarray | dict[str, float] | list[float] | None = None):
        super().__init__(array)

    def get_parameter_index(self, pose_parameter_name: str) -> int:
        return AParametersTha.pose_parameters.get_parameter_index(pose_parameter_name)



def model_input_split(model_input_arr, time_counter):
    return {
        "eyebrow_vector_c": model_input_arr.array[:12],
        "mouth_eye_vector_c": model_input_arr.array[12:12+27],
        "pose_vector_c": model_input_arr.array[12+27:12+27+6],
        "time_counter": time_counter,
    }