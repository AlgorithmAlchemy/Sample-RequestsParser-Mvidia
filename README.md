# MVideo Parser

This project is designed to parse product data from the MVideo website.
It extracts product IDs, names, and prices, and saves them into an SQLite database.

**Read this in other languages:** [Русский (README\_ru.md)](README_ru.md)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/AlgorithmAlchemy/MvidiaRequestsParser.git
   ```

2. Navigate to the project directory:

   ```bash
   cd <project-directory>
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the parser, execute:

```bash
python Parser.py
```

Where `Parser.py` is your main Python script.

When the program starts, you will be prompted to choose an action:

* **Parsing tovar id** – parse product IDs
* **Parsing tovar name** – parse product names
* **Parsing tovar price** – parse product prices
* **Parsing tovar name and price** – parse product names and prices
* **Delete all data and Parsing all data & convert csv** – delete all data, then parse and export to CSV
* **No drop base data - Parsing all data & convert csv** – parse all data and export to CSV without deleting existing records
* **Only convert data to csv** – only convert existing data to CSV
* **Delete all data** – delete all data from the database
* **Delete id base** – delete only product IDs
* **Delete info base (name/price)** – delete only product names and prices
* **Close program** – exit the program

## Notes

* Ensure all required libraries from `requirements.txt` are installed.
* Make sure your cookies and request headers are correctly configured.
