# -*- coding:utf-8 -*- #
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('./user_study.json')
y = df[['user_id','minutes']].groupby('user_id').sum()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('StudyData')
ax.set_xlabel('User ID')
ax.set_ylabel('Study Time')
ax.set_xticks(np.arange(0,230000,23000))
ax.plot(y)
fig.show()
