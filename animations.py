
from abc import abstractmethod
import math
import random

from AnimationStates.animation import Animation, AParameters, AnimationStates, BezierCurveCubic

from .parameters import AParametersTha

from python_utils_aisu.utils import Cooldown


class AnimationStatesTha(AnimationStates):
    def get_parameters_neutral(self) -> AParametersTha:
        """
        This should return a neutral, 0 equivalent, state that animations will add to
        """
        return AParametersTha()

# Static emotions

class Animation_tha(Animation):
    def __post_init__(self):
        self.state = AParametersTha()


class Animation_sentiment_happy_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'sentiment'
        self.sentiments = {'happy': 1.0, **self.sentiments}

        self.state['eyebrow_happy_left'] = 1.0
        self.state['eyebrow_happy_right'] = 1.0

        self.state['mouth_raised_corner_left'] = 0.8
        self.state['mouth_raised_corner_right'] = 0.8


class Animation_sentiment_surprised_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'sentiment'
        self.sentiments = {'surprised': 1.0, **self.sentiments}
        # TODO overshoot transition? default on sentiments

        self.state['eyebrow_raised_left'] = 1.0
        self.state['eyebrow_raised_right'] = 1.0

# Idle animations

class Animation_idle_blinks_random_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_blink'

        if not self.duration:
            self.duration = 0.25

        self.interval = self.fill_default_dict(self.interval, {
            'time': 3.5,
            'variance': 3.3,
        })
        # self.curve_open = BezierCurveCubic.css(0,.57,.5,1)
        self.curve_open = BezierCurveCubic.css(0,.76,1,.77)
        self.curve_close = BezierCurveCubic.css(.92,-0.01,1,.59)
        self.first = 0.2
        self.hold = 0.4

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        elapsed_p = self.elapsed_percent(time_counter)

        if elapsed_p < self.first:
            w = self.curve_close.y((elapsed_p)/(self.first))
        elif elapsed_p < self.first + self.hold:
            w = 1.0
        elif elapsed_p < 1.0:
            other = self.hold + self.first
            w = 1 - self.curve_open.y((elapsed_p - other)/(other))
        else:
            w = 0.0
        self.state['eye_happy_wink_left'] = w
        self.state['eye_happy_wink_right'] = w

class Animation_idle_glance_random_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_glance'

        if not self.duration:
            self.duration = 0.2

        self.interval = self.fill_default_dict(self.interval, {
            'time': 14,
            'variance': 6,
        })

    def init(self):
            direction = random.randint(0, 1)
            if direction == 0:
                direction = -1
            self.random = {
                'iris_rotation_x': direction * random.uniform(0.0, 0.1),
                'iris_rotation_y': direction * random.uniform(0.5, 1.0),
                'head_y': direction * random.uniform(0.0, 0.3),
            }

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        elapsed_p = self.elapsed_percent(time_counter)
        self.state['iris_rotation_x'] = self.random['iris_rotation_x']
        self.state['iris_rotation_y'] = self.random['iris_rotation_y']
        self.state['head_y'] = math.sin(elapsed_p * math.pi) * self.random['head_y']

        if elapsed_p == 1.0:
            self.init()

class Animation_idle_body_still_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_body'

        if not self.duration:
            self.duration = 3


class Animation_idle_body_sway_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_body'

        if not self.duration:
            self.duration = 3

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        tc_pi_duration = self.time_pi_duration(time_counter)

        self.state['neck_z'] = math.sin(tc_pi_duration) * 0.3
        self.state['head_y'] = math.sin(tc_pi_duration) * -0.7
        self.state['body_y'] = math.sin(tc_pi_duration) * 1.0


class Animation_idle_body_head_sway_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_body'

        if not self.duration:
            self.duration = 3

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        tc_pi_duration = self.time_pi_duration(time_counter)

        self.state['neck_z'] = math.sin(tc_pi_duration) * 0.3
        self.state['body_z'] = math.sin(tc_pi_duration) * -0.3

class Animation_idle_body_head_bob_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_body'

        if not self.duration:
            self.duration = 3

        self.lin = None

    def init(self):

        self.lin_prev = self.lin
        self.lin = {
            'head_x': random.uniform(-0.05, -0.1),
            'head_y': random.uniform( 0.3, 0.5),
            'body_y': random.uniform(-0.4, -1.6),
        }
        if not self.lin_prev:
            self.lin_prev = self.lin

        mult = {}
        for key in self.lin.keys():
            mult[key] = (lambda p, value_prev = self.lin_prev[key], value = self.lin[key]: value_prev*(1-p) + value*p)

        self.fun = {
            'head_x': lambda tc_pi_duration, elapsed_p: math.cos(tc_pi_duration * 2) * mult['head_x'](elapsed_p),
            'head_y': lambda tc_pi_duration, elapsed_p: math.cos(tc_pi_duration) * mult['head_y'](elapsed_p),
            'body_y': lambda tc_pi_duration, elapsed_p: math.cos(tc_pi_duration) * mult['body_y'](elapsed_p),
        }

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        tc_pi_duration = self.time_pi_duration(time_counter)
        elapsed_p = self.elapsed_percent(time_counter)
        self.state['head_x'] = self.fun['head_x'](tc_pi_duration, elapsed_p)
        self.state['head_y'] = self.fun['head_y'](tc_pi_duration, elapsed_p)
        self.state['body_y'] = self.fun['body_y'](tc_pi_duration, elapsed_p)
        if elapsed_p == 1.0:
            self.init()

class Animation_idle_breathing_sin_tha(Animation_tha):
    def __post_init__(self):
        super().__post_init__()
        if not self.typ:
            self.typ = 'idle_breathing'

        if not self.duration:
            self.duration = 4

    def animate(self, elapsed, time_counter, **kwargs):
        self.state = AParametersTha()
        tc_pi_duration = self.time_pi_duration(time_counter)

        self.state['breathing'] = abs(math.sin(tc_pi_duration) * 1.0)


Animation.register_classes({
    'Animation_sentiment_happy_tha': Animation_sentiment_happy_tha,
    'Animation_sentiment_surprised_tha': Animation_sentiment_surprised_tha,
    'Animation_idle_blinks_random_tha': Animation_idle_blinks_random_tha,
    'Animation_idle_glance_random_tha': Animation_idle_glance_random_tha,
    'Animation_idle_body_still_tha': Animation_idle_body_still_tha,
    'Animation_idle_body_sway_tha': Animation_idle_body_sway_tha,
    'Animation_idle_body_head_sway_tha': Animation_idle_body_head_sway_tha,
    'Animation_idle_body_head_bob_tha': Animation_idle_body_head_bob_tha,
    'Animation_idle_breathing_sin_tha': Animation_idle_breathing_sin_tha,
})
