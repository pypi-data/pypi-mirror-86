import json

import datetime
import pandas as pd 
import numpy as np 

date1 = pd.to_datetime(datetime.datetime(2020,11,2))
date2 = pd.to_datetime(datetime.datetime(2020,11,8))

a = (date2 - date1) / np.timedelta64(1,'D')

print(a)


--exclude-module tcl --exclude-module tables --exclude-module mpl-data --exclude-module MySQLdb --exclude-module nbconvert --exclude-module notebook --exclude-module PIL --exclude-module psycopg2 --exclude-module pyarrow --exclude-module PyQt5 --exclude-module share
