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

        #try:
        #    import config_keys # Load secret keys
        #    cls.key=config_keys.DATAPOINT_KEY #'648a....df9b'
        #except:
        #    logging.info('Need a datapoint API Key')

        try:
            cls.key=os.environ["DATAPOINT_KEY"]
        except KeyError:
            logging.info('Need a datapoint API Key')

        cls.hrs=hrs
        cls.ProductURI = None

        logging.info("retrieve chart metadata")
        htmlcall_root = 'http://datapoint.metoffice.gov.uk/public/data/image/wxfcs/surfacepressure/xml/capabilities?'
        url = htmlcall_root + str('key=') + str(cls.key)
        try:
            request_raw = requests.get(url)
            data = xmltodict.parse(request_raw.content)['BWSurfacePressureChartList']['BWSurfacePressureChart']

        except ValueError:
            print(f"Failed request for {cls.ofile}")

        try: # find the entry for the target forecast period
            ind = [i for i in range(len(data)) if data[i]['ForecastPeriod'] == str(cls.hrs)][0]
            # Save metadata
            cls.DataDate = data[ind]['DataDate']
            cls.ValidFrom = data[ind]['ValidFrom']
            cls.ProductURI = data[ind]['ProductURI']
            cls.DataDateTime = data[ind]['DataDateTime']
            cls.ForecastPeriod = data[ind]['ForecastPeriod']

            cls.ofile = "docs/charts/" + cls.ValidFrom + "_forecastperiod_" + cls.ForecastPeriod + ".gif"

        except IndexError:
            print(f"Failed request for forecast period {str(cls.hrs)}")
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

            #htmlcall_root = 'http://datapoint.metoffice.gov.uk/public/data/image/wxfcs/surfacepressure/gif?timestep='
            #url = htmlcall_root+str(cls.hrs) + '&key=' + str(cls.key)
            url = cls.ProductURI.replace('{key}',str(cls.key))
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

