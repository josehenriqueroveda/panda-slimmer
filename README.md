# Panda Slimmer
CLI tool to measure the optimization of memory in DataFrame by converting columns to more memory-efficient data types.

<img src="imgs/panda-slimmer-cover.jfif" alt="Panda Slimmer" width="400px"/>

## Description

The script uses the argparse library to parse command line arguments. The `-filename` argument is the path to your file. The `-separator` argument is the CSV separator, which defaults to ','.

## Usage

You can run the script from the command line with the following command:

```bash
python __main__.py -filename <path_to_your_file> -separator <csv_separator>
```

## Example

```bash
python __main__.py -filename data.csv -separator ','
```

Output:

```bash
Initial memory usage: 1.36 MB
Final memory usage: 0.13 MB
Memory savings: 1.23 MB
| COLUMN NAME   | OLD D-TYPE | NEW D-TYPE |
| :------------ | :--------- | :--------- |
| ID            | object     | category   |
| YEAR          | int64      | int16      |
| LOCATION      | object     | category   |
| PRODUCT       | object     | category   |
| CUSTOMER      | object     | category   |
| SAMPLE_DATE   | object     | category   |
| MOISTURE      | float64    | float16    |
| PLANTING_DATE | object     | category   |
| LATITUDE      | float64    | float16    |
| LONGITUDE     | float64    | float16    |
| ENV_TYPE      | object     | category   |
| GDU           | float64    | float16    |
```

## Installation

You can install the required packages with the following command:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Like it? :star: this repository.