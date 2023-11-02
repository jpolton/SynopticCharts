#!/bin/bash
# run wget comment to save surface pressure chart images
# crontab -e
# 30 19 * * * /Users/jelt/GitHub/SynopticCharts/get_MO_charts.sh
# 30 7 * * * /Users/jelt/GitHub/SynopticCharts/get_MO_charts.sh

#source /usr/local/bin/activate /Users/jelt/opt/anaconda3/envs/synoptic_env 
/Users/jelt/opt/anaconda3/bin/conda activate /Users/jelt/opt/anaconda3/envs/synoptic_env
cd /Users/jelt/GitHub/SynopticCharts/
python main.py
conda deactivate