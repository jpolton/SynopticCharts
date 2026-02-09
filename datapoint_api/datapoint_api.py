"""
Get Met Office synoptic charts
Specify the forecast length in hours

Created on 2023-10-31
Updated 2026-02-09 when the API had changed
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


To do:
    * tidy up time handling. Perhaps work with an hours counter, relative to the analysis time, throughout
"""

import os
import requests
import xmltodict
import xml.etree.ElementTree as ET
import xml

import logging
logging.basicConfig(filename='datapoint.log', filemode='w+')
logging.getLogger().setLevel(logging.INFO)

#%% ########## FUNCTIONS ###########################################################



#%% ################################################################################
class CHART():
    """  """
    def __init__(self):
                #hrs: int=0,
                #ofile: str = "output.gif"):

        pass



############ datapoint class methods ##############################################
    @classmethod
    def get_metadata(cls, hrs: int=0):

        """
        URL for plots:
        Midnight analysis:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_00.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_ASXX_Assistant_FC000.gif

        12hr Noon forecast:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_12.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_FSXX_FC012.gif

        Midnight + 24hr forecast:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_24.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_FSXX_FC024.gif

        Noon +36hr forecast:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_36.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_MEDIUM_RANGE_FC036.gif

        Midnight +48hr forecast
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_48.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_MEDIUM_RANGE_FC048.gif

        Noon +60hr forcast:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_60.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_MEDIUM_RANGE_FC060.gif

        Midnight +72hr forecast:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_72.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_MEDIUM_RANGE_FC072.gif

        Noon +84hr forecast:
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/colour/2026-02-09T0000/FSXX00T_84.gif
        https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_MEDIUM_RANGE_FC084.gif
        """
        
        forecast_periods = [0, 12, 24, 36, 48, 60, 72, 84]

        cls.hrs=hrs
        cls.ProductURI = None

        logging.info("retrieve chart metadata")
        url = 'https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw'
        try:
            request_raw = requests.get(url)
            data = request_raw.json()
            # print(request_raw.content)
        except ValueError:
            print(f"Failed request for {cls.hrs}")
            return

        try: 
            # find the entry for the target forecast period
            products = data['products']
            target_product = None
            search_str = f"FC{int(hrs):03d}"
            
            for product in products:
                if search_str in product['uri']:
                    target_product = product
                    break
            
            if target_product:
                cls.DataDate = target_product['data_date']
                cls.ProductURI = target_product['uri']
                
                # Extract filename from URI to match the form in line 77 (e.g. 0000_FSXX_FC024.gif)
                #filename = cls.ProductURI.split('/')[-1]
                filename = cls.DataDate + "_forecastperiod_" + str(cls.hrs) + ".gif"
                cls.ofile = f"docs/charts/{filename}"
            else:
                raise IndexError("Forecast period not found")

        except (IndexError, KeyError) as e:
            print(f"Failed request for forecast period {str(cls.hrs)}: {e}")
            pass

        return

#########################################################
    @classmethod
    def get_chart(cls,
                  hrs: int=0,
                  ofile: str = None):

        """
        desc
        Save gif file

        INPUTS:
            hrs : int
            ofile : str

        OUTPUT:
            None
        """


        cls.hrs=hrs
        if ofile != None:
            cls.ofile = ofile

        cls.get_metadata(hrs = hrs)

        check_file = os.path.isfile(cls.ofile)
        if (not check_file) and (cls.ProductURI is not None):
            logging.info("retrieve chart")


            #https://data.consumer-digital.api.metoffice.gov.uk/v1/surface-pressure/bw/2026-02-09T0000/0000_FSXX_FC012.gif

            url = cls.ProductURI #.replace('{key}',str(cls.key))
            try:
                request_raw = requests.get(url)
                print(request_raw.status_code)
                with open(cls.ofile, 'wb') as out:
                    out.write(request_raw.content)

            except ValueError:
                print(f"Failed request for {cls.ofile}")
        else:
            if(check_file):
                print(f"File {cls.ofile} already exists")
            if(cls.ProductURI is None):
                print(f"Forecast {cls.hrs} does not exist")

        return

