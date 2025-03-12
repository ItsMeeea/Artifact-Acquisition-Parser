import os
import json
import subprocess
import logging
from regipy.registry import RegistryHive

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Paths – adjust these paths as necessary
OFFLINE_HIVES_DIR = r"D:\Lab3_RegistryDumps"      # Directory where offline registry hive files are stored
OUTPUT_DIR = r"D:\Lab3_ParsedRegistry"             # Directory where parsed output and CSV results will be saved
RECMD_PATH = r"D:\School\RECmd\RECmd.exe"            # Path to the RECmd executable

# List of registry hives to process
HIVES = ["SAM", "SYSTEM", "SOFTWARE", "SECURITY", "NTUSER.DAT"]

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Helper function to convert bytes to a hex string
def bytes_to_hex(o):
    if isinstance(o, bytes):
        return o.hex()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


# Function to parse offline registry hives
def parse_offline_registry():
    parsed_data = {}
    for hive in HIVES:
        hive_path = os.path.join(OFFLINE_HIVES_DIR, hive)
        if os.path.exists(hive_path):
            try:
                reg_hive = RegistryHive(hive_path)
                hive_data = {}
                # Recursively iterate through subkeys and collect their values
                for subkey in reg_hive.recurse_subkeys():
                    values = {}
                    for value in subkey.values:
                        # Convert bytes to hex string if necessary
                        if isinstance(value.value, bytes):
                            values[value.name] = value.value.hex()
                        else:
                            values[value.name] = value.value
                    hive_data[subkey.path] = values
                parsed_data[hive] = hive_data
                logging.info(f"[+] Successfully parsed {hive}.")
            except Exception as e:
                logging.error(f"[-] Error parsing hive {hive}: {e}")
        else:
            logging.error(f"[-] Hive file {hive_path} not found.")
    # Save the parsed data to a JSON file using a custom serializer for bytes
    output_file = os.path.join(OUTPUT_DIR, "offline_registry.json")
    with open(output_file, "w") as f:
        json.dump(parsed_data, f, indent=4, default=bytes_to_hex)
    logging.info(f"[+] Offline registry data saved to {output_file}")
    return parsed_data


# Function to run RECmd.exe on each hive and generate CSV output
def run_rec_cmd():
    for hive in HIVES:
        hive_path = os.path.join(OFFLINE_HIVES_DIR, hive)
        if os.path.exists(hive_path):
            cmd = [RECMD_PATH, "-f", hive_path, "--csv", OUTPUT_DIR]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                logging.info(f"[+] RECmd output for {hive}:\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                logging.error(f"[-] Error running RECmd on {hive}: {e.stderr}")
        else:
            logging.error(f"[-] Hive file {hive_path} not found for RECmd.")


def main():
    logging.info("[+] Starting Offline Registry Processing...")
    parse_offline_registry()
    run_rec_cmd()
    logging.info("[+] Offline Registry Processing Completed.")


if __name__ == "__main__":
    main()
