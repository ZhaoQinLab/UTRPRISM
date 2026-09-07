#!/usr/bin/env python3
"""Custom layers required to deserialize the frozen Keras model."""

from __future__ import annotations

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


@keras.utils.register_keras_serializable(package="UTRPRISM")
class ReduceSum(layers.Layer):
    def __init__(self, axis: int, **kwargs):
        super().__init__(**kwargs)
        self.axis = axis

    def call(self, inputs):
        return tf.reduce_sum(inputs, axis=self.axis)

    def get_config(self):
        return {**super().get_config(), "axis": self.axis}


@keras.utils.register_keras_serializable(package="UTRPRISM")
class BilinearInteraction(layers.Layer):
    def __init__(self, units: int, **kwargs):
        super().__init__(**kwargs)
        self.units = units

    def build(self, input_shape):
        self.proj_a = layers.Dense(self.units, name=f"{self.name}_proj_a")
        self.proj_b = layers.Dense(self.units, name=f"{self.name}_proj_b")

    def call(self, inputs):
        first, second = inputs
        return self.proj_a(first) * self.proj_b(second)

    def get_config(self):
        return {**super().get_config(), "units": self.units}


CUSTOM_OBJECTS = {
    "ReduceSum": ReduceSum,
    "BilinearInteraction": BilinearInteraction,
}
