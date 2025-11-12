"""
Ce module calcule un indice de feu normalisé à partir des bandes infrarouges
IR_112 et IR_039 issues de produits satellitaires (GOES / MTG).

Inspiré du travail original de Léa Boulvard à Météo-France :
- IR_112 (≈ 10.5 µm) : sensible à la température de surface.
- IR_039 (≈ 3.9 µm) : sensible aux hautes températures (feux).
"""

import numpy as np


def prepare_ir112(ir112_raw):
    """
    Prépare la bande IR_112 (≈ 10.5 µm) pour le calcul de l'indice.
    Dans les produits Météo-France, les valeurs sont en Kelvin.
    On applique une normalisation linéaire de 183.15K à +150K au-dessus (~333K).

    Sortie : array 16 bits entre 1 et 65535.
    """
    ir112_mod = np.maximum(1, np.minimum(65535, (65535 * ((ir112_raw - 183.15) / 150))))
    return ir112_mod


def prepare_ir039(ir039_raw):
    """
    Prépare la bande IR_039 (≈ 3.9 µm) pour le calcul de l'indice.
    Application d’un gamma 0.4 comme dans le code original.
    """
    ir039_mod = np.maximum(1, np.minimum(65535, 65535 * ((ir039_raw - 273.15) / 60) ** (1.0 / 0.4)))
    return ir039_mod


def compute_fire_index_from_arrays(ir112_mod, ir039_mod, gamma=0.4, bit_depth=16):
    """
    Calcule l'indice normalisé à partir des bandes IR préparées.

    - ratio_initial_bis : rapport normalisé des deux canaux (évite division par 0)
    - inversion du signe : feux = valeurs élevées
    - gamma correction
    - normalisation [0, 65535] ou [0, 255]
    """
    # Évite les divisions par zéro
    denom = ir112_mod + ir039_mod
    denom[denom == 0] = np.nan

    ratio_initial_bis = (ir112_mod - ir039_mod) / denom
    ratio_16b = -ratio_initial_bis  # feux -> valeurs hautes

    # Normalisation 0–1
    ratio_norm = (ratio_16b - np.nanmin(ratio_16b)) / (np.nanmax(ratio_16b) - np.nanmin(ratio_16b))

    # Application du gamma
    ratio_gamma = ratio_norm ** (1.0 / gamma)

    # Passage en 8 ou 16 bits
    maxv = 65535 if bit_depth == 16 else 255
    ratio_scaled = ratio_gamma * maxv

    # Nettoyage et conversion
    ratio_scaled = np.nan_to_num(ratio_scaled, nan=0)
    ratio_scaled = ratio_scaled.astype(np.uint16 if bit_depth == 16 else np.uint8)

    return ratio_scaled


def compute_index_from_raw(ir112_raw, ir039_raw, bit_depth=16):
    """
    Fonction principale utilisée par run_full_processing.py

    - Convertit les bandes IR brutes en versions "normalisé"
    - Calcule l'indice à partir de ces bandes
    - Retourne un tableau d'entiers (8 ou 16 bits)
    """
    ir112_mod = prepare_ir112(ir112_raw)
    ir039_mod = prepare_ir039(ir039_raw)

    idx = compute_fire_index_from_arrays(
        ir112_mod,
        ir039_mod,
        gamma=0.4,
        bit_depth=bit_depth
    )

    return idx
