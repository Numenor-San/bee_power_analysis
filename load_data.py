import argparse
import pandas as pd

def load_data(path):
    df = pd.read_excel(path)
    df = df[df['Capped_Brood'].notna()]
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/2025_capp_brood(protein-nutrition).xlsx")
    args = parser.parse_args()

    new_df = load_data(args.data)
