
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,date
import plotly.plotly as py
import plotly.graph_objs as go
from itertools import product
import plotly.figure_factory as ff
import ast

class lhdata():
    def __init__(self):
        self.edges = pd.read_csv('checkedge.csv')
        self.edges = self.edges.rename(columns = {'Jul-15 to Aug08': 'CurrMonth'})
        self.col = 'CurrMonth'
        series = pd.Series([ast.literal_eval(i) for i in self.edges['areabrkup']])
        srdf= pd.DataFrame(series, columns = ['AreaSplit'])
        self.edges = self.edges.merge(srdf, left_index=True, right_index=True)
        ix = self.edges.index
        self.edges.loc[ix,'Origin_Destn'] = self.edges.loc[ix,'Origin']+'_'+self.edges.loc[ix,'Destn']
        self.startdate = datetime.strptime('15-07-2017','%d-%m-%Y')
        self.enddate = datetime.strptime('08-08-2017','%d-%m-%Y')
        self.orglist = list(self.edges['Origin'].unique())
        self.destlist = list(self.edges['Destn'].unique())
        self.orgoptions = [{'label': i, 'value': i} for i in self.orglist]
        self.destoptions = [{'label': i, 'value': i} for i in self.destlist]


    def lh_printfigs (self,orglist,destlist):
        edges = self.edges
        reporttitle = 'Linehaul Edge Data'
        fl = edges[(edges['Origin'].isin(orglist))&(edges['Destn'].isin(destlist))]
        bl = edges[(edges['Origin'].isin(destlist))&(edges['Destn'].isin(orglist))]
        df = fl.append(bl)
        data = [
            go.Bar(
                x=df['Origin_Destn'].values, # assign x as the dataframe column 'x'
                y=df['CurrMonth'].values
            )]
        layout = go.Layout(
            barmode='stack',
            title=reporttitle
        )

        fig = go.Figure(data=data, layout=layout)
        annotations = []
        for count,i in enumerate(fig.data[0].get('y')):
            annotations.append(dict(x = fig.data[0].get('x')[count], y=np.round(i,2)+2,text = np.round(i,1),showarrow=False))
        fig.layout['annotations'] = annotations
        heatmaplist = []
        for org,dest,areasplit in zip(df['Origin'],df['Destn'],df['AreaSplit']):
            for area in list(areasplit.keys()):
                item = [area.split('-')[0],area.split('-')[1],areasplit.get(area)]
                heatmaplist.append(item)
        heatmapdf = pd.DataFrame(heatmaplist, columns=['OrgArea','DestArea','Wt']).dropna()
        heatmappivot = heatmapdf.pivot_table(index = 'OrgArea', values = 'Wt', columns = 'DestArea', aggfunc = pd.np.sum)
        heatmappivot = heatmappivot.fillna(0.0).T
        x = list(heatmappivot.columns)
        y = list(heatmappivot.index)
        z = heatmappivot.values
        z_text = np.around(z,decimals=1)
        heatmapfig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')
        for i in range(len(heatmapfig.layout.annotations)):
            heatmapfig.layout.annotations[i].font.size = 10

        heatmapfig.layout.title = 'Load Table in Mt'
        heatmapfig.layout.yaxis.title='Destination Area'
        heatmapfig.layout.xaxis.title='Origin Area'
        heatmapfig.layout.xaxis.side='bottom'
        return fig,heatmapfig



    def returngraphs(self,orglist,destlist):
        return self.lh_printfigs(orglist,destlist)
