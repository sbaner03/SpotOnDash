import pandas as pd
import numpy as np
from datetime import datetime,timedelta,date

class duedatediag:
    def __init__(self):
        dd = pd.read_csv('duedatediag.csv')
        #### replace with a query to a database
        dd = dd.rename( columns={"DOCKNO": "Failed", "TOTAL": "Total"})
        dd['Org'] = dd.apply(lambda x: x['specific_pt'].split('-')[0],axis=1)
        dd['Dest'] = dd.apply(lambda x: x['specific_pt'].split('-')[1],axis=1)
        virtuallocs = ['AMCF','AMDO','BBIB','BDQB','IXGF','BLRF','BWDB','BRGO','CCC','CJBC','DELO','GZBB','HYDO','IDRB','JAIC','JLRB','KNB','LKOB','MAAC','NAGB','PLGB','PNQO','PNQK','RPRB','SMBF','SNRB','VPIB','VGAF','SLMF','BHOB']
        dd['Reason'] = dd.apply(lambda x: 'Virtual' if x['Org'] in virtuallocs or x['Dest'] in virtuallocs else x['Reason'], axis=1)
        dd['Date'] = dd.apply(lambda x: datetime.strptime(x['Timestamp'],"%Y-%m-%d"),axis=1)
        loclist = list(dd['Org'].unique())+list(dd['Dest'].unique())

        startdate = min(dd['Date'])
        enddate = max(dd['Date'])
        #### color mapping of regions to locations
        self.dd = dd
        self.loclist = loclist
        self.startdate = startdate
        self.enddate = enddate
        self.threshold = (enddate-startdate).days
