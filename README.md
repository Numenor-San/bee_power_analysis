# Bee Brood Power Analysis

Power analysis for honeybee brood experiments.

Code and data to reproduce the power analyses for the paper:
Gonçalves RFS, de Sousa RT, Stabler D, Pinto DMS, Wright GA, Shafir S.  
*A technical semi-field methodology to measure the effect of nutrition on honeybee brood rearing*.  
Journal of Experimental Biology, Methods & Techniques. DOI: 10.1242/jeb.251151  

Also available on bioRxiv: https://doi.org/10.1101/2025.07.01.662504

---

## Installation


Run the command bellow in a terminal to Clone the repository and create the Conda environment:
```bash
git clone https://github.com/Numenor-San/bee_power_analysis.git
cd bee_power_analysis
conda env create -f environment.yml
```
Activate the environment
```bash
conda activate JEB
```

## Usage
This is part of a technical semi-field method to quantify the proteins influence on the colony's capacity to rear its brood (aka make new bees).

This repository implements the power analysis used to estimate how many colonies per diet are needed to detect the protein effect on brood production at a given confidence level; 80% is usually enough.<br>

This follows the conditions described in the paper. In brief:<br>
- **Environmental conditions**
  - Temperature: avg ~20°C (10–30°C)
  - Humidity: ~70%
- **Colony requirements**
  - 1000–1600 nurse bees
  - Mated egg-laying queen

You can upload your data in the data folder, just change the "2025_data.xlsx" and run this code in the terminal
```bash
python bee_power_analysis.py
```
Alternatively you can iterate the conditions directly in the python script.

The script:<br>
1. Loads the brood vs protein dataset from data/2025_capp_brood(protein-nutrition).xlsx<br>
2. Fits an Ordinary Least Squares (OLS) model: capped brood ~ protein<br>
3. Computes Cohen’s f from the model R²<br>
4. Uses statsmodels to estimate:<br>
   Achieved power at the current sample size<br>
   Required sample size to reach 80% power<br>

## Model
We use an Ordinary Least Squares (OLS) regression model with protein percentage as predictor and capped brood as response, and derive Cohen’s f from the model R² for F-test power calculations.