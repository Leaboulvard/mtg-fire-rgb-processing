"""
utils.py
Fonctions utilitaires : normalisation, verification output_path
"""
import numpy as np
import rasterio
import os
from rasterio.transform import from_origin

def normalize_band_custom(band, in_min, in_max, gamma=1.0, bit_depth=16, floor=0, ceil=None):
    """
    Normalisation
    band: numpy array (float, values raw)
    in_min/in_max: entrée (ex: for IR_112 use -90->60°C -> converted in K handling upstream)
    gamma: gamma to apply (1 = linear)
    bit_depth: 16 or 8
    floor: minimum output before casting (for 16bit you used 1 to avoid zeros)
    ceil: if provided, overrides computed max scaling
    """
    # Compute scaled [0..1] then gamma and scale to bit depth
    # Avoid division by zero:
    denom = (in_max - in_min) if (in_max - in_min) != 0 else 1.0
    norm = (band - in_min) / denom
    norm = np.clip(norm, 0.0, 1.0)
    if gamma != 1.0:
        # apply gamma as in your code: **(1/gamma) used before
        norm = norm ** (1.0 / gamma)
    maxv = 65535 if bit_depth == 16 else 255
    out = norm * maxv
    if floor is not None:
        out = np.maximum(out, floor)
    if ceil is not None:
        out = np.minimum(out, ceil)
    out = np.nan_to_num(out, nan=0)
    return out.astype(np.uint16 if bit_depth == 16 else np.uint8)


def ensure_output_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path
