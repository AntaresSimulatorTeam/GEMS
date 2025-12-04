from pathlib import Path

import pandas as pd



def get_objective_value(file_name: Path) -> float:
    match file_name.suffix:
        case ".csv":
            df = pd.read_csv(file_name, usecols=["output", "value"])
            result = df.query("output == 'OBJECTIVE_VALUE'")["value"]
            return float(result.iloc[0])
        case ".tsv":
            df = pd.read_csv(file_name, sep="\t", usecols=["output", "value"])
            result = df.query("output == 'OBJECTIVE_VALUE'")["value"]
            return float(result.iloc[0])
        case _:
            raise ValueError(f"Invalid file format: {file_name.suffix}")