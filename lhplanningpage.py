import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
from spotonLH import lhdata



glyph = html.Div(className = 'glyphicon glyphicon-glass')
def makepage_lhplanning(orgoptions,destoptions,startdate,enddate,lhgraph,lhheatmap):
    app = dash.Dash()
    #### html elements
    title = html.H1(className = "h3",children='LH Edge and Area Data {0} to {1}'.format(startdate.date(),enddate.date()))
    displaydiv = html.Div(className = 'container-fluid',children=[
        html.Div(className = 'title', children = title),
        dcc.Graph(id='lhgraph',figure = lhgraph),
        dcc.Graph(id='lhheatmap',figure = lhheatmap)])

    selectiondiv = html.Div(className = 'container-fluid', children=[
    html.Img(className="img-responsive",
        src = 'http://www.spoton.co.in/images/spoton.jpg'),
    html.Br(),
    html.Label('Select Origin'),
    dcc.Dropdown(
        id = 'org_selection',
        options=orgoptions, #### reason
        value=['BLRH'],
        multi = True
    ),
    html.Br(),
    html.Label('Select Destination'),
    dcc.Dropdown(
        id = 'dest_selection',
        options=destoptions,
        value=['DELH'],
        multi = True
    )])

    app.layout = html.Div(className='row', children=[html.Div(className = 'col-sm-2',children = [selectiondiv]),html.Div(className= 'col-sm-10',children = [displaydiv])])
    return app.layout
