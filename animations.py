
import math

from AnimationStates.animation import Animation, AParameters

from .parameters import AParametersTha

from python_utils_aisu.utils import Cooldown

# Static emotions

class Animation_tha_happy(Animation):
    def __post_init__(self):
        if not self.type:
            self.type = 'sentiment' 
        self.sentiments = {'happy': 1.0, **self.sentiments}

        self.state = AParametersTha()
        self.state['eyebrow_happy_left'] = 1.0
        self.state['eyebrow_happy_right'] = 1.0

        self.state['mouth_raised_corner_left'] = 0.8
        self.state['mouth_raised_corner_right'] = 0.8


class Animation_tha_surprised(Animation):
    def __post_init__(self):
        if not self.type:
            self.type = 'sentiment' 
        self.sentiments = {'surprised': 1.0, **self.sentiments}
        # TODO overshoot transition? default on sentiments
        self.state = AParametersTha()
        self.state['eyebrow_raised_left'] = 1.0
        self.state['eyebrow_raised_right'] = 1.0

# Idle animations

class Animation_tha_idle_blinks_random(Animation):
    def __post_init__(self):
        if not self.type:
            self.type = 'idle_blink'

        if not self.time:
            self.time = 0.2

        self.interval = {
            'time': 7,
            'variance': 2,
            **self.interval,
        }

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        elapsed_p = self.elapsed_percent(elapsed)
        self.state['eye_happy_wink_left'] = math.sin(elapsed_p * math.pi) * 0.1
        self.state['eye_happy_wink_right'] = math.sin(elapsed_p * math.pi) * 1.0


class Animation_tha_idle_glance_random(Animation):
    def __post_init__(self):
        if not self.type:
            self.type = 'idle_glance'

        if not self.time:
            self.time = 0.2

        self.interval = {
            'time': 7,
            'variance': 2,
            **self.interval,
        }

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        elapsed_p = self.elapsed_percent(elapsed)
        self.state['iris_rotation_x'] = math.sin(elapsed_p * math.pi) * 0.1
        self.state['iris_rotation_y'] = math.sin(elapsed_p * math.pi) * 0.8

        self.state['head_y'] = math.sin(elapsed_p * math.pi) * 0.6


class Animation_tha_idle_body_sway(Animation):
    def __post_init__(self):
        if not self.type:
            self.type = 'idle_body'

        if not self.time:
            self.time = 3

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        tc_pi_duration = self.time_pi_duration(time_counter)

        self.state['neck_z'] = math.sin(tc_pi_duration) * 0.3
        self.state['body_y'] = math.sin(tc_pi_duration) * 1.0


class Animation_tha_idle_breathing_sin(Animation):
    def __post_init__(self):
        if not self.type:
            self.type = 'idle_breathing'

        if not self.time:
            self.time = 4

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        tc_pi_duration = self.time_pi_duration(time_counter)

        self.state['breathing'] = abs(math.sin(tc_pi_duration) * 1.0)


Animation.register_classes({
    'Animation_tha_happy': Animation_tha_happy,
    'Animation_tha_surprised': Animation_tha_surprised,
    'Animation_tha_idle_blinks_random': Animation_tha_idle_blinks_random,
    'Animation_tha_idle_glance_random': Animation_tha_idle_glance_random,
    'Animation_tha_idle_body_sway': Animation_tha_idle_body_sway,
    'Animation_tha_idle_breathing_sin': Animation_tha_idle_breathing_sin,
})
