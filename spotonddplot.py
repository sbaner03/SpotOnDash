import pandas as pd
import numpy as np
from datetime import datetime,timedelta,date
import plotly.plotly as py
import plotly.graph_objs as go

def dd_generatepivot(df,reason,org):
    df = df[df['Reason']==reason]
    if org ==['All']:
        orglist = list(df['Org'].unique())
    else:
        orglist = org
        df = df[df['Org'].isin(orglist)]
    pivot = df.pivot_table(index = ['specific_pt','Org'], values = ['Total','Failed'], aggfunc=np.sum).reset_index()
    pivot['Perc'] = pivot.apply(lambda x: np.round(x['Failed']*100.0/x['Total'],2),axis=1)
    pivot = pivot.sort_values(['Failed', 'Total'], ascending=[False, False])
    return pivot

def dd_printfigs(df,reason,org,threshold,virtuallocs):
    pivot = dd_generatepivot(df,reason,org)
    finalperc = np.round(pivot['Failed'].sum()*100.0/pivot['Total'].sum(),2)
    total = pivot['Total'].sum()
    pivot = pivot[pivot['Total']>=threshold]

    data = []
    for counter, org in enumerate(pivot['Org'].unique()):
        if reason == 'Virtual' and org in virtuallocs:
            markerdata = dict(size = 10,color = 'rgb(255,69,0,0.9)')
        elif reason == 'Virtual':
            markerdata = dict(size = 10,color = 'rgba(27, 224, 68, 0.7)')
        else:
            markerdata = dict(size = 10) ### map the regioncode here later
        trace = go.Scatter(
            x = pivot[pivot['Org']==org]['Failed'],
            y = pivot[pivot['Org']==org]['Perc'],
            name = org,
            mode = 'markers',
            marker = markerdata,
            ### the color should be linked to the org's region for location
            text= pivot[pivot['Org']==org]['specific_pt']
            )
        data.append(trace)


    layout = dict(title = '{0} failure {1}% out of {2} cons'.format(reason,np.round(finalperc,0),total),
                    paper_bgcolor = '#FFFAFA',
                    plot_bgcolor = '#FFFAFA',
                  yaxis = dict(title = 'Failure Percentage', zeroline = True),
                  xaxis = dict(title = 'Failed Cons', zeroline = True)
                 )

    fig = dict(data=data, layout=layout)
    return fig
