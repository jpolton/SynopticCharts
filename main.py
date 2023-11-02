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
#from datapoint_api import CHART
from datapoint_api.datapoint_api import CHART



if __name__ == '__main__':

    #datetime.datetime.now()
    # Load in data from the Datapoint API. Analysis is obtained by default

    for hrs in ['0', '12', '24', '36', '48', '60', '72', '84', '96', '120']:
        tt = CHART()
        #hrs = 12
        #tt.get_chart( hrs=hrs, ofile="charts/output"+str(hrs)+".gif")
        tt.get_chart( hrs=hrs)



