# SynopticCharts
Download Met Office sea level pressure synoptic charts twice a day and present in a [table](https://jpolton.github.io/SynopticCharts/index.html). The table has the time for which the forecast is made increaing to the right and the newest forecast being the top row.

<img width="706" alt="synoptic_chart_layout" src="https://github.com/jpolton/SynopticCharts/assets/22616872/9c46d8dd-b5b5-4dad-bfb6-4fec7ce11bb6">

There is a two step process:
1) fetch the charts, using the Met Office datapoint API, twice a day. This is done with a GitAction. The charts are stored in `docs/charts/`
2) Render the charts in a table using javascript: `docs/index.html`

## Run jobs locally
Instead of running GitActions to obtain the charts, a cronjob could be run locally. A cronjob script might look like:

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
