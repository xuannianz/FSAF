"""
Copyright 2017-2018 Fizyr (https://fizyr.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import keras

import numpy as np
import math


class PriorProbability(keras.initializers.Initializer):
    """ Apply a prior probability to the weights.
    """

    def __init__(self, probability=0.01):
        """
        Initialize the probability.

        Args:
            self: (todo): write your description
            probability: (todo): write your description
        """
        self.probability = probability

    def get_config(self):
        """
        Returns a dictionary of configuration.

        Args:
            self: (str): write your description
        """
        return {
            'probability': self.probability
        }

    def __call__(self, shape, dtype=None):
        """
        Return the probability at the given shape.

        Args:
            self: (todo): write your description
            shape: (tuple): write your description
            dtype: (todo): write your description
        """
        # set bias to -log((1 - p)/p) for foreground
        result = np.ones(shape, dtype=dtype) * -math.log((1 - self.probability) / self.probability)

        return result
