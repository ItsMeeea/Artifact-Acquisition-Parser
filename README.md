# Offline Windows Registry Hive Parser

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)](https://opensource.org/licenses/)
[![Regipy](https://img.shields.io/badge/Uses-regipy-blue)](https://github.com/mkorman90/regipy)
[![RECmd](https://img.shields.io/badge/Uses-RECmd-blue)](https://github.com/EricZimmerman/RECmd)

This project is a Python-based offline registry parser that processes Windows registry hive files using both the `regipy` library and [RECmd](https://github.com/EricZimmerman/RECmd) — a command-line tool from Eric Zimmerman's forensics toolkit.

It is built for digital forensics labs, system analysis, and educational purposes.

---

## Features

- Parses the following offline registry hive files:
  - `SAM`
  - `SYSTEM`
  - `SOFTWARE`
  - `SECURITY`
  - `NTUSER.DAT`
- Extracts keys and values recursively using `regipy`
- Converts binary registry values into hex strings
- Outputs structured JSON with full registry paths and values
- Runs `RECmd.exe` to generate CSV reports for each hive
- Logs all actions with timestamps and error reporting

---

## Requirements

- Python 3.7+
- [regipy](https://github.com/mkorman90/regipy)
- [RECmd](https://github.com/EricZimmerman/RECmd)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/registry-hive-parser.git
cd registry-hive-parser
```

2. Install dependencies:

```bash
pip install regipy
```

3. Download RECmd:

Visit [https://ericzimmerman.github.io/](https://ericzimmerman.github.io/) and download RECmd. Extract it and take note of the full path to `RECmd.exe`.

---

## Configuration

Open the `registry_parser.py` script and edit the following paths at the top:

```python
OFFLINE_HIVES_DIR = r"D:\Lab3_RegistryDumps"       # Directory where hive files are stored
OUTPUT_DIR = r"D:\Lab3_ParsedRegistry"             # Output directory for JSON and CSV
RECMD_PATH = r"D:\School\RECmd\RECmd.exe"          # Full path to RECmd.exe
```

Make sure your registry hive files (`SAM`, `SYSTEM`, `SOFTWARE`, `SECURITY`, `NTUSER.DAT`) are placed in the directory specified by `OFFLINE_HIVES_DIR`.

---

## Usage

To run the script, execute:

```bash
python registry_parser.py
```

The script will:

- Parse each hive using `regipy` and generate a JSON file (`offline_registry.json`) containing all key-value pairs.
- Run RECmd on each hive to produce CSV reports for detailed forensic analysis.

---

## Output

After execution, the output directory will contain:

- `offline_registry.json` — combined structured output from `regipy`
- One or more `.csv` files — RECmd analysis for each hive

Example directory structure:

```
D:\Lab3_ParsedRegistry\
│
├── offline_registry.json
├── SAM.csv
├── SYSTEM.csv
├── SOFTWARE.csv
├── SECURITY.csv
└── NTUSER.DAT.csv
```

---

## Logging

The script uses Python’s `logging` module and provides timestamped logs in the console:

```
2025-04-30 12:00:00 - INFO - [+] Successfully parsed SAM.
2025-04-30 12:00:01 - ERROR - [-] Hive file SYSTEM not found.
```

You can modify `logging.basicConfig()` in the script to redirect logs to a file if desired.

---

## Code Overview

The script consists of:

- **`parse_offline_registry()`**: Uses `regipy` to parse and serialize all keys/values to JSON.
- **`run_rec_cmd()`**: Invokes `RECmd.exe` on each hive to generate CSV output.
- **`main()`**: Calls both functions and manages execution flow.

Helper functions are used to convert binary data into hex strings for JSON compatibility.

---

## License

This project is provided for **educational and forensic research purposes only**. Use responsibly and within legal and ethical boundaries.

## Credits

- [regipy](https://github.com/mkorman90/regipy) by @mkorman90  
- [RECmd](https://github.com/EricZimmerman/RECmd) by Eric Zimmerman
