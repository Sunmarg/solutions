
import dash                              # pip install dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *
init_notebook_mode()
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import calendar
from pandas import Timestamp

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets9.lottiefiles.com/private_files/lf30_5ttqPi.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets9.lottiefiles.com/packages/lf20_8wREpI.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
url_reactions = "https://assets2.lottiefiles.com/packages/lf20_nKwET0.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


# Import App data from csv sheets **************************************
data = pd.read_csv("help_desk_data-2.csv")
from datetime import datetime
for i in range(0,len(data["when assigned"])):
    if( type(data["when assigned"][i]) != float) :   
        data["when assigned"][i] = datetime.strptime(data["when assigned"][i], '%d-%b-%Y %H:%M:%S')
        data["when assigned"][i]=datetime.date(data["when assigned"][i])
for i in range(0,len(data["when closed"])):
    if( type(data["when closed"][i]) != float) :   
        data["when closed"][i] = datetime.strptime(data["when closed"][i], '%d-%b-%Y %H:%M:%S')
        data["when closed"][i]=datetime.date(data["when closed"][i])
        
d=data.copy()
d=d[d["when closed"].notna()]
d=d[d["when assigned"].notna()]
d["Time Taken"]=0
d.reset_index(inplace=True)
d.drop(["index"],axis=1,inplace=True)
for i in range(0,len(d["when assigned"])):
    d["Time Taken"][i]=(d["when closed"][i]-d["when assigned"][i]).days
d["Time Taken Y"]=0
d.reset_index(inplace=True)
d.drop(["index"],axis=1,inplace=True)
for i in range(0,len(d["when assigned"])):
    d["Time Taken Y"][i]=d["when assigned"][i].year

for i in range(0,len(d["when assigned"])):  
        d["when assigned"][i] = pd.Timestamp(d["when assigned"][i])
        d["when closed"][i] = pd.Timestamp(d["when closed"][i])
      
d['Month Assigned']=0
for i in range(0,len(d['Month Assigned'])):
    d['Month Assigned'][i]=d['when assigned'][i].month
d['Month Closed']=0
for i in range(0,len(d['Month Closed'])):
    d['Month Closed'][i]=d['when closed'][i].month

items = [
    dbc.DropdownMenuItem("5"),
    dbc.DropdownMenuItem("10"),
    dbc.DropdownMenuItem("15"),
    
]
op=[{'label':x, 'value':x} for x in sorted(d.ticket_type.unique())]
op.append({'label':'All Data', 'value':'All'})


# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                 meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=0.5,'}]
               )


app.layout = dbc.Container([
       dbc.Row(
        dbc.Col(html.H1("Help-Desk Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
    
    dbc.Row([
         dbc.Col([
           html.Div([html.Label(['Date Range:'],style={'font-weight': 'bold', "text-align": "center"}),

                     dcc.DatePickerSingle(
                        id='my-date-picker-start',
                        date=date(2018, 1, 1),
                        display_format='MMM Do, YYYY',  # how selected dates are displayed in the DatePickerRange component.
                        month_format='MMMM, YYYY',
                        className='ml-2'
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-end',
                        date=date(2021, 4, 4),
                        display_format='MMM Do, YYYY',  # how selected dates are displayed in the DatePickerRange component.
                        month_format='MMMM, YYYY',
                        className='mb-2 ml-2'
                   ) 
                ]),
                
            
        ], xs=12, sm=4, md=6, lg=3, xl=3),
        dbc.Col(
            
            [html.Div([html.Label(['Choose Ticket Type:'],style={'font-weight': 'bold', "text-align": "center"}),
                        
            
              dcc.Dropdown(id='ticket_type',
                 options=op,
                 value='All_',
                 placeholder='Ticket Type..',
                 
                 style={'width':'100%'}
                 )
             ])
            ]
             
        ,xs=12, sm=4, md=6, lg=3, xl=3),
        dbc.Col([html.Div([html.Label(['Choose Solver:'],style={'font-weight': 'bold', "text-align": "center"}),
                        
            
              dcc.Dropdown(id='solver',
                 options=[],
                 value='All_',
                 
                 placeholder='Select Solver..',
                 style={'width':'100%'}
                 )])
        ],xs=12, sm=4, md=6, lg=3, xl=3),
        dbc.Col(
            
            [html.Div([html.Label(['Choose Priority:'],style={'font-weight': 'bold', "text-align": "center"}),
                        
            
               dcc.Dropdown(id='pridrop', placeholder='Priority...',
                                     options=[{'label': 'Low', 'value': 'LOW'},
                                              {'label': 'Medium', 'value': "MEDIUM"},{'label': 'High', 'value': 'HIGH'},{'label':'All Data','value':'All_'}],value='All',disabled=False,                     #disable dropdown value selection
            multi=False,  
            searchable=True),
                 
             ])
            ]
             
        ,xs=12, sm=4, md=6, lg=3, xl=3),
             
        
       ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Total Tickets Raised'),
                    html.H2(id='content-connections', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], xs=12, sm=4, md=4, lg=2, xl=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Total Requestors'),
                    html.H2(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], xs=12, sm=4, md=4, lg=2, xl=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Ticket Solvers'),
                    html.H2(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], xs=12, sm=4, md=4, lg=2, xl=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="53%", height="53%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Avg Ticket Solving time'),
                    html.H2(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], xs=12, sm=4, md=4, lg=2, xl=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_reactions)),
                dbc.CardBody([
                    html.H6('Total Tickets Closed'),
                    html.H2(id='content-reactions', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], xs=12, sm=4, md=4, lg=2, xl=2),
    ],className='mb-2'),
    dbc.Row([
       
        dbc.Col([
            
            dcc.Dropdown(id='dropdown', placeholder='Minimum Tasks...',
                                     options=[{'label': 'Minimum Tasks: 0', 'value': 0},
                                         {'label': 'Minimum Taks: 5', 'value': 5},
                                              {'label': 'Minimum Taks: 10', 'value': 10},{'label': 'Minimum Taks: 15', 'value': 15}],value=-1,disabled=False,                     #disable dropdown value selection
            multi=False,  
            searchable=True),
           
                        
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart-1', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        
            
        ], xs=12, sm=7, md=12, lg=7, xl=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart-2', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], xs=12, sm=5, md=12, lg=5, xl=5),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='horizontal', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], xs=12, sm=4, md=6, lg=4, xl=4),
        dbc.Col([
           
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart-3', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], xs=12, sm=3, md=6, lg=3, xl=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='sunburst-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], xs=12, sm=5, md=10, lg=5, xl=5),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='month', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], xs=12, sm=12, md=12, lg=12, xl=12)
      
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='data', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], xs=12, sm=12, md=12, lg=12, xl=12)
      
    ],className='mb-2')
        
], fluid=True)

@app.callback(
    Output('solver','options')    ,
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('pridrop','value')
)
def options(start_date,end_date,ttype,prior):
    
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    
    dff_c = d.copy()

    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    t=dff_c['Assigned To'].unique()
    ip=[{'label':x, 'value':x} for x in sorted(t)]
    ip.append({'label':'All Data', 'value':'All'})
    return ip
# Updating the 5 number cards ******************************************
@app.callback(
    Output('content-connections','children'),
    Output('content-companies','children'),
    Output('content-msg-in','children'),
    Output('content-msg-out','children'),
    Output('content-reactions','children'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
    
)

def update_small_cards(start_date, end_date,ttype,stype,prior):
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    
    dff_c = d.copy()

    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    conctns_num = len(dff_c)
    compns_num = len(dff_c['requestor name'].unique())

   
    in_num = len(dff_c['Assigned To'].unique())
    dff_c = d.copy() 
    dff_r = dff_c[(dff_c['when closed']>=start_date) & (dff_c['when closed']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_r=dff_r[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_r=dff_r[dff_c['Assigned To']==stype]  
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_r=dff_r[dff_c['priority']==prior]
    reactns_num = len(dff_r)
    a=dff_r['Time Taken'].sum()
    out_num=round(a/reactns_num,2)
    return conctns_num, compns_num, in_num, out_num, reactns_num


# Line Chart ***********************************************************
@app.callback(
    Output('bar-chart-1','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('dropdown','value'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
  
)
def update_bar_chart_1(start_date, end_date,tasks,ttype,stype,prior):
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    dff_c = d.copy()
    if(tasks<0):
        tasks=0
    date1=start_date.strftime("%d/%m/%Y")
    date2=end_date.strftime("%d/%m/%Y")
   
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    d2=dff_c.copy()
    df1=d2.groupby('Assigned To').agg({'Time Taken':'sum'})
    count_series = d2.groupby(['Assigned To']).size()
    new_df = count_series.to_frame(name = 'size').reset_index()
    df1=df1.reset_index()
    result = pd.merge(df1, new_df, on='Assigned To')
    result['Avg Time Taken']=0
    for i in range(0,len(result['size'])):
        result['Avg Time Taken'][i]=result['Time Taken'][i]/result['size'][i]
    
    result=result[result['size']>=tasks]
    fig = go.Figure(
        data=[
            go.Bar(name='Count of tickets', x=result['Assigned To'].tolist(), y=result['size'], yaxis='y', offsetgroup=1),
            go.Bar(name='Average Time Taken', x=result['Assigned To'].tolist(), y=result['Avg Time Taken'], yaxis='y2', offsetgroup=2)
        ],
        layout={
            'yaxis': {'title': 'Count of tickets'},
            'yaxis2': {'title': 'Average Time Taken', 'overlaying': 'y', 'side': 'right'}
        }
        )
    if(tasks>0):
        fig.update_layout(barmode='group',title="Solvers with minimum of "+str(tasks)+" tasks completed")
    else:
        fig.update_layout(barmode='group',title="All Solvers from " +str(date1)+ " to "+ str(date2))
    fig.update_layout(showlegend=False)
   # fig.update_traces(mode="lines+markers", fill='tozeroy',line={'color':'blue'})
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig

# Bar Chart ************************************************************
@app.callback(
    Output('bar-chart-2','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
)
def update_bar_chart_2(start_date, end_date,ttype,stype,prior):
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    dff_c = d.copy()
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    d1=dff_c.copy()
    count_series = d1.groupby(['requestor name','Time Taken Y']).size()
    new_df = count_series.to_frame(name = 'size').reset_index()
    
    new_df=new_df.sort_values(by='size',ascending=False).iloc[:5,:]
    fig = px.bar(new_df, y='size', x='requestor name',hover_data=['size'], labels={'size':'count of tickets'},title='Top requestors')

    fig.update_xaxes(tickangle=-45)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig.update_traces(marker_color='blue')
  
    return fig


# Pie Chart ************************************************************
@app.callback(
    Output('sunburst-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
)
def update_sunburst(start_date, end_date,ttype,stype,prior):
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    dff_c = d.copy()
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    df=dff_c.copy()
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    df['Count of tickets']=1  
   
    fig = px.sunburst(df, path=['ticket_type', 'ticket_subtype'], values='Count of tickets')
    
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig.update_layout(title="Ticket Types & Subtypes")
    
    return fig


# Word Cloud ************************************************************
@app.callback(
    Output('data','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
)
def update_data(start_date, end_date,ttype,stype,prior):
    
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    date1=start_date.strftime("%d/%m/%Y")
    date2=end_date.strftime("%d/%m/%Y")
    dff_c = d.copy()
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    df=dff_c.copy()
    cols=df.columns[:-4]
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(cols),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df['client'].tolist(), df['requestor name'].tolist(), df['priority'].tolist(), df['status'].tolist(), df['Assigned To'].tolist(),
       df['when assigned'].tolist(), df['when closed'].tolist(), df['ticket_type'].tolist(), df['ticket_subtype'].tolist(),
       df['ticket_category'].tolist(), df['subject'].tolist()],
               fill_color='lavender',
               align='left'))
        ])
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig.update_layout(title='Data from '+str(date1)+' to '+ str(date2))
    return fig

@app.callback(
    Output('bar-chart-3','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
)
def update_bar_chart_3(start_date, end_date,ttype,stype,prior):
    
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    dff_c = d.copy()
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    df=dff_c.copy()
    
    
    
    count_series_1= df.groupby(['ticket_subtype']).size()
    pied = count_series_1.to_frame(name = 'size').reset_index()
  
    pied=pied.sort_values(by='size',ascending=False).iloc[:3,:]
    fig = px.bar(pied, x='ticket_subtype', y='size',hover_data=['size'], labels={'size':'count of tickets'},title="Top Subtype Counts")
    
    fig.update_xaxes(tickangle=-45)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

@app.callback(
    Output('horizontal','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
)
def update_horizontal(start_date, end_date,ttype,stype,prior):
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    dff_c = d.copy()
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    df=dff_c.copy()

    count_series = df.groupby(['priority']).size()
    new_df = count_series.to_frame(name = 'size').reset_index()
    fig = px.bar(new_df, x='size', y='priority',hover_data=['size'], labels={'size':'count of tickets'},title="Priority Vs Ticket Count",orientation=('h'))
   
   
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

@app.callback(
    Output('month','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
    Input('ticket_type','value'),
    Input('solver','value'),
    Input('pridrop','value')
)

def update_month(start_date, end_date,ttype,stype,prior):
    start_date=pd.Timestamp(start_date)
    end_date=pd.Timestamp(end_date)
    dff_c = d.copy()
    dff_c = dff_c[(dff_c['when assigned']>=start_date) & (dff_c['when assigned']<=end_date)]
    if (ttype=='All' or ttype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['ticket_type']==ttype]
    if (stype=='All' or stype=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['Assigned To']==stype]
    if (prior=='All' or prior=="All_"):
        pass
    else:
        dff_c=dff_c[dff_c['priority']==prior]
    df=dff_c.copy()
    ordered_months = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"]
    h=df.groupby(['Month Assigned','Time Taken Y']).size().reset_index().groupby(['Month Assigned','Time Taken Y'])[[0]].max()
    h=h.reset_index()
    h = h.sort_values(by="Month Assigned")
    h['Month Assigned'] = h['Month Assigned'].apply(lambda x: calendar.month_name[x])
    
    h.columns=['Month Assigned','Time Taken Y', 'Count of Tickets']
    h.sort_values(by='Month Assigned',inplace=True)
    h['to_sort']=h['Month Assigned'].apply(lambda x:ordered_months.index(x))
    h= h.sort_values('to_sort')
    fig = px.bar(h, x="Month Assigned", y='Count of Tickets', color="Time Taken Y", title='Tickets Raised VS Month w.r.t Year')
    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

if __name__=='__main__':
    app.run_server(debug=False, port=8004)