import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
from dash.dependencies import Input, Output

from duediagpage import makepage_dd
from spotonDD import duedatediag
from spotonddplot import dd_generatepivot
from spotonddplot import dd_printfigs

from lhplanningpage import makepage_lhplanning
from spotonLH import lhdata




app = dash.Dash()

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.supress_callback_exceptions = True
my_css_url = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app.css.append_css({
    "external_url": my_css_url
})


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go to Due Date Diagnostic', href='/page_dddiag'),
    html.Br(),
    dcc.Link('Go to LH Planning', href='/page_lhplanning'),
])

page_dddiag_layout = makepage_dd()
ddobj =duedatediag()
dd = ddobj.dd
startdate = ddobj.startdate
enddate = ddobj.enddate
dd = dd[(dd['Date']>=startdate)&(dd['Date']<=enddate)]
threshold = ddobj.threshold
virtuallocs = ddobj.virtuallocs
dd_fig = dd_printfigs(dd,'Virtual',['All'],threshold,virtuallocs)
table = ff.create_table(dd_generatepivot(dd.head(10),'Virtual',['All']))

@app.callback(
    Output(component_id='org_selector',component_property = 'options'),
    [Input(component_id='reason_selection', component_property='value')]
)
def updatedropdown(reason):
    if reason == 'Virtual':
        orgoptions = [i for i in ddobj.orgoptions if i['value'] in virtuallocs or i['value']=='All'] 
    else:
        orgoptions = [i for i in ddobj.orgoptions]
    return orgoptions


@app.callback(
    Output(component_id='graph',component_property = 'figure'),
    [Input(component_id='reason_selection', component_property='value'),
    Input(component_id='org_selector', component_property='value')]
)
def updatechart(reason,org):
    dd_fig = dd_printfigs(dd,reason,org,threshold,virtuallocs)
    return dd_fig

@app.callback(
    Output(component_id='table',component_property = 'figure'),
    [Input(component_id='reason_selection', component_property='value'),
    Input(component_id='table_filter', component_property='value'),
    Input(component_id='org_selector', component_property='value')]
)
def updatechart2(reason,table_filter,org):
    pivot = dd_generatepivot(dd,reason,org)
    pivot = pivot.rename(columns = {'specific_pt': 'Lane'})
    if table_filter=='All':
        pass
    elif table_filter=='Top10':
        pivot = pivot.head(10)
    else:
        pivot = pivot.head(25)

    table = ff.create_table(pivot)
    return table


lh = lhdata()
lhgraph,lhheatmap = lh.returngraphs(['BLRH'],['DELH'])
page_lhplanning_layout = makepage_lhplanning(lh.orgoptions,lh.destoptions,lh.startdate,lh.enddate,lhgraph,lhheatmap)

@app.callback(
    Output(component_id='lhgraph',component_property = 'figure'),
    [Input(component_id='org_selection', component_property='value'),
    Input(component_id='dest_selection', component_property='value')]
)
def updatelhchart(orglist,destlist):
    lhgraph,lhheatmap = lh.returngraphs(orglist,destlist)
    return lhgraph

@app.callback(
    Output(component_id='lhheatmap',component_property = 'figure'),
    [Input(component_id='org_selection', component_property='value'),
    Input(component_id='dest_selection', component_property='value')]
)
def updatelhchart2(orglist,destlist):
    lhgraph,lhheatmap = lh.returngraphs(orglist,destlist)
    return lhheatmap


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page_dddiag':
        return page_dddiag_layout
    elif pathname == '/page_lhplanning':
        return page_lhplanning_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here



if __name__ == '__main__':
    app.run_server(debug=True)
