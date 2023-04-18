# Tiqets Assignment

## Setup
Create and activate virtual environment
```shell
python3 -m venv venv
source venv/bin/activate
```

Install required packages
```shell
pip install -r requirements.txt
```

## Usage
Example usage
```shell
python -m generator -o "data/orders.csv" -b "data/barcodes.csv" -p "data/output.csv"
```

Use `python -m generator --help` to see help message

## Testing
In order to run tests in `tests` folder run
```shell
python -m unittest discover tests --pattern "test_*.py"
```
