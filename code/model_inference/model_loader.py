#!/usr/bin/env python3
"""Load and validate the frozen production model."""

from __future__ import annotations

from pathlib import Path

from tensorflow import keras

from custom_layers import CUSTOM_OBJECTS


EXPECTED_INPUTS = {
    "utr_sequence": (None, 6000, 4),
    "utr_coverage": (None, 6000, 1),
    "mirna_sequence": (None, 30, 4),
}


def load_production_model(path: str | Path):
    model = keras.models.load_model(
        Path(path), custom_objects=CUSTOM_OBJECTS, compile=False, safe_mode=False
    )
    observed = {tensor.name.split(":")[0]: tuple(tensor.shape) for tensor in model.inputs}
    if observed != EXPECTED_INPUTS:
        raise ValueError(f"Unexpected model signature: {observed}")
    if len(model.outputs) != 1 or tuple(model.outputs[0].shape) != (None, 1):
        raise ValueError(f"Unexpected model output: {[tuple(x.shape) for x in model.outputs]}")
    return model
