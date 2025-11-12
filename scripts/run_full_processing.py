import argparse
import os
import xarray as xr
import numpy as np
from skimage import io

# Import des fonctions de calcul
from scripts.compute_fire_index import compute_index_from_raw
from scripts.utils import ensure_output_dir


def main():
    parser = argparse.ArgumentParser(description="Process GOES/MTG NetCDF to RGB composites")
    parser.add_argument("--input", required=True, help="Chemin du fichier NetCDF (.nc)")
    parser.add_argument("--out", required=True, help="Dossier de sortie")
    parser.add_argument("--bits", type=int, choices=[8, 16], default=16, help="Profondeur en bits (8 ou 16)")
    parser.add_argument("--mode", choices=["day", "night"], default="day", help="Mode de composition RGB")

    args = parser.parse_args()
    input_file = args.input
    output_dir = args.out
    bit_depth = args.bits
    mode = args.mode

    # === 1. Chargement du dataset ===
    print(f"Ouverture du fichier : {input_file}")
    ds = xr.open_dataset(input_file)

    # === 2. Extraction des bandes utilisées ===
    print("Extraction des bandes nécessaires...")
    VIS_008 = ds["VIS_008"].values
    VIS_006 = ds["VIS_006"].values
    VIS_004 = ds["VIS_004"].values
    VIS_022 = ds["VIS_022"].values
    VIS_016 = ds["VIS_016"].values
    IR_039 = ds["IR_039"].values
    IR_112 = ds["IR_112"].values

    # === 3. Calcul de l'indice de feu ===
    print("Calcul de l’indice de feu...")
    ratio_16bits = compute_index_from_raw(IR_112, IR_039, bit_depth=bit_depth)

    # === 4. Normalisation des canaux visibles ===
    print("Normalisation des bandes visibles...")
    VIS_008_norm = np.maximum(0, np.minimum(65535, (65535 * (VIS_008 / 100))))
    VIS_004_norm = np.maximum(0, np.minimum(65535, (65535 * (VIS_004 / 100))))
    VIS_022_norm = np.maximum(0, np.minimum(65535, (65535 * (VIS_022 / 100))))
    VIS_016_norm = np.maximum(0, np.minimum(65535, (65535 * (VIS_016 / 75))))

    VIS_008_16bits = VIS_008_norm.astype(np.uint16)
    VIS_004_16bits = VIS_004_norm.astype(np.uint16)
    VIS_022_16bits = VIS_022_norm.astype(np.uint16)
    VIS_016_16bits = VIS_016_norm.astype(np.uint16)

    # === 5. Création de la composition RGB ===
    if mode == "day":
        print("🌞 Création de la composition RGB jour...")
        composite_rgb = np.stack([ratio_16bits, VIS_008_16bits, VIS_004_16bits], axis=-1)
        output_name = "composite_day_fire_16b.tif"
    else:
        print("🌙 Création de la composition RGB nuit...")
        composite_rgb = np.stack([ratio_16bits, VIS_022_16bits, VIS_016_16bits], axis=-1)
        output_name = "composite_night_fire_16b.tif"

    # === 6. Sauvegarde ===
    ensure_output_dir(output_dir)
    output_path = os.path.join(output_dir, output_name)
    print(f"💾 Enregistrement de l’image : {output_path}")
    io.imsave(output_path, composite_rgb)

    print("✅ Traitement terminé avec succès !")

if __name__ == "__main__":
    main()
