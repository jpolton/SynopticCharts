"""
Get Met Office synoptic charts using datapoint API
Specify the forecast length in hours

Created on 2023-10-31
@author: jelt

Python environment:

    ### Build python environment:
    ## Create an environment with coast installed
    yes | conda env remove --name synoptic_env
    yes | conda create --name synoptic_env python=3.9
    conda activate synoptic_env

    ## install request for datapoint server requests
    yes | conda install -c conda-forge requests xmltodict

Example usage:
    from datapoint_api.datapoint_api import GAUGE
    tt = CHART()
    tt.get_chart( hrs=0, ofile= "most_recent_analysis.gif")
"""

import sys, os
import logging
import datetime
import json
import re
import shutil

sys.path.append(os.path.dirname(os.path.abspath("datapoint_api/datapoint_api.py")))

try:
    from datapoint_api import CHART
except:
    from datapoint_api.datapoint_api import CHART

# Set up logging, consistent with datapoint_api/datapoint_api.py
LOG_FILE = os.environ.get("SYNOPTIC_LOG", "log.txt")
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    force=True,
)
logger = logging.getLogger("synoptic")

def move_old_files(source_folder, target_folder, keep=100):
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # List all files in the source folder
    files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    # Sort files by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Get the files to move (all but the newest 'keep' files)
    files_to_move = files[keep:]

    # Move the files
    for file_path in files_to_move:
        shutil.move(file_path, target_folder)
        logger.info(f"Moved: {file_path} -> {target_folder}")


def load_forecast_metadata(metadata_path, legacy_path):
    if os.path.isfile(metadata_path):
        with open(metadata_path, encoding="utf-8") as source:
            return json.load(source)

    forecasts_by_issue = {}
    if os.path.isfile(legacy_path):
        legacy_line = re.compile(
            r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s*:\s*"
            r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s*\+\s*(\d+)hrs"
        )
        with open(legacy_path, encoding="utf-8") as source:
            for line in source:
                match = legacy_line.fullmatch(line.strip())
                if not match:
                    continue
                issued, target_date, forecast_lead = match.groups()
                forecast = forecasts_by_issue.setdefault(
                    issued, {"issued": issued, "products": []}
                )
                forecast["products"].append({
                    "target_date": target_date,
                    "forecast_lead": int(forecast_lead),
                })

    return list(forecasts_by_issue.values())


def save_forecast_metadata(metadata_path, forecasts_by_issue, keep=6):
    forecasts = sorted(
        forecasts_by_issue.values(),
        key=lambda forecast: forecast["issued"],
        reverse=True,
    )[:keep]
    with open(metadata_path, "w", encoding="utf-8") as destination:
        json.dump(forecasts, destination, indent=2)
        destination.write("\n")


if __name__ == '__main__':

    #datetime.datetime.now()
    # Load in data from the Datapoint API. Analysis is obtained by default
    forecast_periods = [0, 12, 24, 36, 48, 60, 72, 84, 96, 120]
    metadata_path = "docs/forecast_metadata.json"
    forecasts = load_forecast_metadata(metadata_path, "docs/issue_timestamp.txt")
    forecasts_by_issue = {forecast["issued"]: forecast for forecast in forecasts}


    for hrs in forecast_periods:
        tt = CHART()
        #hrs = 12
        #tt.get_chart( hrs=hrs, ofile="charts/output"+str(hrs)+".gif")
        tt.get_chart( hrs=hrs)
        if tt.ProductURI is not None:
            forecast = forecasts_by_issue.setdefault(
                tt.Issued_timestamp,
                {"issued": tt.Issued_timestamp, "products": []},
            )
            forecast["products"] = [
                product for product in forecast["products"]
                if product["target_date"] != tt.DataDate
            ]
            forecast["products"].append({
                "target_date": tt.DataDate,
                "forecast_lead": hrs,
            })

    save_forecast_metadata(metadata_path, forecasts_by_issue)

    source_folder = "docs/charts"
    target_folder = "docs/charts/archive"
    move_old_files(source_folder, target_folder, keep=50)


