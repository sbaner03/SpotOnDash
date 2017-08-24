from datetime import datetime,timedelta,date
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
from spotonDD import duedatediag
from spotonddplot import generatepivot
from spotonddplot import printfigs


app = dash.Dash()
# Append an externally hosted CSS stylesheet

app.config.supress_callback_exceptions = True


ddobj =duedatediag()
dd = ddobj.dd
startdate = ddobj.startdate
enddate = ddobj.enddate
dd = dd[(dd['Date']>=startdate)&(dd['Date']<=enddate)]
threshold = ddobj.threshold
virtuallocs = ddobj.virtuallocs
fig = printfigs(dd,'Virtual',['All'],threshold,virtuallocs)
table = ff.create_table(generatepivot(dd.head(10),'Virtual',['All']))

#### html elements
title = html.H1(className = "h3",children='Due Date Diagnostic from {0} to {1}'.format(startdate.date(),enddate.date()))

displaydiv = html.Div(className = 'container-fluid',children=[
    html.Div(className = 'row', children =
    html.Div(className = 'col-sm-12', children = [title])),
    dcc.Graph(id='graph',figure = fig),
    dcc.Graph(id='table',figure = table)
])



selectiondiv = html.Div(className = 'container-fluid', children=[
html.Img(className="img-responsive",
    src = 'http://www.spoton.co.in/images/spoton.jpg'),
html.Br(),
html.Label('Select Reason'),
dcc.Dropdown(
    id = 'reason_selection',
    options=ddobj.reasonoptions, #### reason
    value='Virtual'
),
html.Br(),
html.Label('Select # of Rows'),
dcc.Dropdown(
    id = 'table_filter',
    options=ddobj.tableoptions,
    value='Top10',
),
html.Br(),
html.Label('Select Origin'),
dcc.Dropdown(
id = 'org_selector',
options = ddobj.orgoptions,
value = ['All'],
multi = True)])

app.layout = html.Div(className='row', children=[html.Div(className = 'col-sm-2',children = [selectiondiv]),html.Div(className= 'col-sm-10',children = [displaydiv])])

@app.callback(
    Output(component_id='graph',component_property = 'figure'),
    [Input(component_id='reason_selection', component_property='value'),
    Input(component_id='org_selector', component_property='value')]
)
def updatechart(reason,org):
    fig = printfigs(dd,reason,org,threshold,virtuallocs)
    return fig

@app.callback(
    Output(component_id='table',component_property = 'figure'),
    [Input(component_id='reason_selection', component_property='value'),
    Input(component_id='table_filter', component_property='value'),
    Input(component_id='org_selector', component_property='value')]
)
def updatechart2(reason,table_filter,org):
    pivot = generatepivot(dd,reason,org)
    pivot = pivot.rename(columns = {'specific_pt': 'Lane'})
    if table_filter=='All':
        pass
    elif table_filter=='Top10':
        pivot = pivot.head(10)
    else:
        pivot = pivot.head(25)

    table = ff.create_table(pivot)
    return table


app.run_server(debug=True)
