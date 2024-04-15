import json
import argparse
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")


def read_data(filepath: str, separator=","):
    """
    Reads data from a CSV or XLSX file into a DataFrame.

    Args:
        filepath (str): Path to the file.
        separator (str): CSV separator. Default is ','.

    Returns:
        DataFrame: The data from the file.
    """
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath, sep=separator)
    elif filepath.endswith(".xlsx"):
        return pd.read_excel(filepath)
    else:
        raise ValueError("File must be a CSV or Excel file.")


def convert_dtypes(df: pd.DataFrame):
    """
    Converts DataFrame columns to more memory-efficient dtypes.

    Args:
        df (DataFrame): The DataFrame to convert.

    Returns:
        DataFrame: The converted DataFrame.
    """
    dtype_conversions = {
        "object": "category",
        "int64": np.int16,
        "float64": np.float16,
    }

    for column, dtype in df.dtypes.items():
        if str(dtype) in dtype_conversions.keys():
            df[column] = df[column].astype(dtype_conversions[str(dtype)])

    return df


def create_cli_table(df: pd.DataFrame, old_dtypes):
    """
    Creates a CLI table showing column name, old dtype, and new dtype.

    Args:
        df (DataFrame): The DataFrame to create the table for.
        old_dtypes (list): The old dtypes of the DataFrame.

    Returns:
        str: The CLI table.
    """
    cli_table = pd.DataFrame()
    rows = []

    for column, old_dtype, new_dtype in zip(df.columns, old_dtypes, df.dtypes):
        rows.append([column, old_dtype, new_dtype])

    cli_table = pd.DataFrame(
        rows, columns=["COLUMN NAME |", "OLD D-TYPE |", "NEW D-TYPE"]
    )

    return cli_table


def save_dtypes(df: pd.DataFrame, output_path="dtypes.json"):
    """
    Saves the dtypes of a DataFrame to a JSON file.

    Args:
        df (DataFrame): The DataFrame to save the dtypes of.
        output_path (str): The path to save the JSON file to.
    """
    dtypes = df.dtypes.astype(str).to_dict()
    with open(output_path, "w") as f:
        json.dump(dtypes, f)


def optimize_dataframe(filepath: str, separator=","):
    """
    Optimizes a DataFrame by converting columns to more memory-efficient dtypes.

    Args:
        filepath (str): Path to the file.
        separator (str): CSV separator. Default is ','.

    Returns:
        tuple: A tuple containing:
            - float: Memory savings in bytes after optimization.
            - str: CLI table showing column name, old dtype, and new dtype.
    """
    df = read_data(filepath, separator)
    initial_memory = (df.memory_usage(deep=True).sum()) / 1024**2
    old_dtypes = df.dtypes.tolist()

    df = convert_dtypes(df)

    final_memory = (df.memory_usage(deep=True).sum()) / 1024**2
    memory_savings = initial_memory - final_memory

    cli_table = create_cli_table(df, old_dtypes)

    return df, initial_memory, final_memory, memory_savings, cli_table


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        CLI tool to measure the optimization of memory in DataFrame by converting columns to more memory-efficient data types, 
        then output a json file with the data types mapping.

        ╭─ Example ───────────────────────────────────────────────────────────╮
        | $ python panda-slimmer -file "data.csv" -sep "," -o "dtypes.json"   |
        ╰─────────────────────────────────────────────────────────────────────╯
        
        Developed by: Jose Henrique Roveda
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-file", type=str, help=">> Path to the file (CSV or XLSX).")
    parser.add_argument(
        "-sep",
        type=str,
        default=",",
        help=" >> (Optional) CSV separator. Default is ','.",
    )
    parser.add_argument(
        "-o",
        type=str,
        default=None,
        help=" >> (Optional) Output path to save the dtypes of the optimized DataFrame.",
    )

    args = parser.parse_args()

    df, initial_memory, final_memory, memory_savings, cli_table = optimize_dataframe(
        args.file, args.sep
    )

    print(f"Initial memory usage: {initial_memory:.2f} MB")
    print(f"Final memory usage: {final_memory:.2f} MB")
    print(f"Memory savings: {memory_savings:.2f} MB")
    print(cli_table.to_markdown(index=False))

    if args.o:
        save_dtypes(df, args.o)
        print(f"Data types mapping saved to {args.o}")
