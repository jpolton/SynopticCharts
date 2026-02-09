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
sys.path.append(os.path.dirname(os.path.abspath("datapoint_api/datapoint_api.py")))
import datetime
import shutil
try:
    from datapoint_api import CHART
except:
    from datapoint_api.datapoint_api import CHART

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
        print(f"Moved: {file_path} -> {target_folder}")


if __name__ == '__main__':

    #datetime.datetime.now()
    # Load in data from the Datapoint API. Analysis is obtained by default
    forecast_periods = [0, 12, 24, 36, 48, 60, 72, 84]


    for hrs in forecast_periods:
        tt = CHART()
        #hrs = 12
        #tt.get_chart( hrs=hrs, ofile="charts/output"+str(hrs)+".gif")
        tt.get_chart( hrs=hrs)

    source_folder = "docs/charts"
    target_folder = "docs/charts/archive"
    move_old_files(source_folder, target_folder, keep=100)



