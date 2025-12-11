# Bee Brood Power Analysis
Power analysis for honeybee brood experiments:

Code and data to reproduce the power analyses for the paper:
Gonçalves RFS, de Sousa RT, Stabler D, Pinto DMS, Wright GA, Shafir S.  
*A technical semi-field methodology to measure the effect of nutrition on honeybee brood rearing*.  
Journal of Experimental Biology, Methods & Techniques. DOI: 10.1242/jeb.251151	
Also available on bioRXiv: doi: https://doi.org/10.1101/2025.07.01.662504

## Installation
```bash
git clone https://github.com/<your-user>/bee-brood-power-analysis.git
cd bee-brood-power-analysis
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r dependencies.yml
```

## Usage
This is part of a technical semi-field method to quantify the protein % influence on the colony's capacity to rear its brood (aka make new bees).
The purpose of the power analysis is to quantify how many replicates the scientist will need to detect a protein effect at a given degree of confidence; 80% is usually enough.<br>

Following the method described in the paper, key environmental metrics should be followed:<br>
Ambient Temperature: avg 20 °C. min 10°C max 30°C<br>
Humidity: avg 70%<br>
And Colony population metrics:<br> 
Honey Bee Nurses: min 1000 max 1600<br>
Egg-laying Queen presence:  always<br>

````
conda env create -f environment.yml
conda activate JEB
python bee_power_analysis.py
````

## Model
We used an Ordinary Least Squares Model