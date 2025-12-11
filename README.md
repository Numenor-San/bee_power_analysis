# Bee Brood Power Analysis

Power analysis for honeybee brood experiments.

Code and data to reproduce the power analyses for the paper:

Gonçalves RFS, de Sousa RT, Stabler D, Pinto DMS, Wright GA, Shafir S.  
*A technical semi-field methodology to measure the effect of nutrition on honeybee brood rearing*.  
Journal of Experimental Biology, Methods & Techniques. DOI: 10.1242/jeb.251151  
Also available on bioRxiv: https://doi.org/10.1101/2025.07.01.662504

---

## Installation

Clone the repository and create the Conda environment:

```bash
git clone https://github.com/Numenor-San/bee_power_analysis.git
cd bee_power_analysis

conda env create -f environment.yml
conda activate JEB
```
## Usage
This is part of a technical semi-field method to quantify the protein % influence on the colony's capacity to rear its brood (aka make new bees).

This repository implements the power analysis used to estimate how many colonies per diet are needed to detect an effect of protein percentage on capped brood production at a given confidence level; 80% is usually enough.<br>

```bash
python bee_power_analysis.py
```

This follows the conditions described in the paper. In brief:<br>
Environmental conditions<br>
    Ambient temperature: avg ~20 °C (min 10 °C, max 30 °C)<br>
    Relative humidity: avg ~70%<br>
Colony conditions<br>
    Honey bee nurses: ~1000–1600 per mini-colony<br>
    Egg-laying queen: present in all colonies<br>

The script:<br>
1/ Loads the brood vs protein dataset from data/2025_capp_brood(protein-nutrition).xlsx<br>
2/ Fits an Ordinary Least Squares (OLS) model: capped brood ~ protein<br>
3/ Computes Cohen’s f from the model R²<br>
4/ Uses statsmodels to estimate:<br>
    Achieved power at the current sample size<br>
    Required sample size to reach 80% power<br>

## Model
We use an Ordinary Least Squares (OLS) regression model with protein percentage as predictor and capped brood as response, and derive Cohen’s f from the model R² for F-test power calculations.