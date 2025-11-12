# 🛰️ MTG Fire & RGB Processing  
### *(GOES-16 Example for Meteosat Third Generation Workflows)*

---

🇬🇧 **EN — Project Description**  
This repository contains Python scripts to process **multispectral satellite data (GOES-16)** to generate:  
 **Fire Index** (based on IR3.9 µm and IR11.2 µm)  
 **Daytime RGB composites** (True Color + Fire Temperature RGB)  

The workflow reproduces the MTG (Meteosat Third Generation) imagery pipeline developed during a research internship at **Météo-France**.  
Since MTG data are not publicly distributed, **GOES-16 NetCDF scenes** are used as open-source analogs for demonstration.

---

🇫🇷 **FR — Description du projet**  
Ce dépôt regroupe des scripts Python permettant de traiter des **données multispectrales satellitaires (GOES-16)** afin de générer :  
 Un **indice feu** (bande IR 3.9 µm et IR 11.2 µm)  
 Des **composites RGB de jour** (True Color + Fire Temperature RGB)  

Le pipeline reproduit la méthodologie de traitement développée lors d’un stage à **Météo-France** pour la mission **MTG**.  
Les données GOES-16 servent ici d’exemple libre pour démontrer la logique appliquée aux produits MTG (non publics).

---

## Project Structure
mtg-fire-rgb-processing/
│
├── data/ # Input NetCDF files (.nc) [ignored by Git]
├── outputs/ # Output GeoTIFFs or RGB composites
├── scripts/
│ ├── init.py
│ ├── compute_fire_index.py
│ ├── run_full_processing.py
│ └── utils.py
├── requirements.txt
└── README.md


---

## Installation & Dependencies

### Requirements
- Python ≥ 3.9  
- `numpy`, `xarray`, `rasterio`, `GDAL`, `scikit-image`  
- Optional: `matplotlib` for quick visualization  

### Installation
```bash
conda create -n MTG python=3.11
conda activate MTG
pip install -r requirements.txt
```

---

## Usage

### Placer votre fichier NetCDF GOES-16** dans le dossier `data/`  
(exemple : `data/Emultic2kmNC4_goes16_202307141700.nc`)  

Ce fichier correspond à la scène du **14 juillet 2023 à 17h00 UTC**, au moment où plusieurs **feux de forêt au Canada** étaient clairement visibles depuis le satellite GOES-16.  
Il a été utilisé comme **cas d’étude principal** pour valider le calcul de l’indice feu et la génération des composites RGB.  

> ⚠️ Pour des raisons de taille et de licence, le fichier `.nc` **n’est pas inclus** dans le dépôt GitHub.  
> Cependant, un **exemple du résultat final** (image composite RGB produite à partir de cette scène) est disponible dans le dossier `outputs/`.  


### Lancer le pipeline de traitement complet
```bash
python -m scripts.run_full_processing --input data/Emultic2kmNC4_goes16_202307141700.nc --out outputs --bits 16 --mode day
```

### Résultats (output)
Les fichiers GeoTIFF et les images RGB générés sont automatiquement enregistrés dans le dossier outputs/.

---

## Notes
Le code utilise des formules simplifiées inspirées des traitements pré-opérationnels de la mission MTG.

Le fichier compute_fire_index.py gère le prétraitement des bandes IR 3.9 µm et IR 11.2 µm ainsi que le calcul de l’indice feu.

Le fichier utils.py est responsable de la normalisation, de la conversion en 8 ou 16 bits, et de l’export en GeoTIFF.

---

## Auteur
Léa — développé dans le cadre d’un stage à Météo-France (2025).
(Projet à visée éducative et démonstrative — workflow équivalent à celui de MTG, appliqué sur des données publiques GOES-16.)