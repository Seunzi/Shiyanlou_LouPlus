# -*- coding: utf-8 -*- #

import json
import pandas as pd

def analysis(file,user_id):
    times = 0
    minutes = 0

    jdf = pd.read_json(file)
    times = jdf[jdf['user_id'] == user_id].count()['user_id']
    minutes = jdf[jdf['user_id'] == user_id]['minutes'].sum()

    return times,minutes
