import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output


# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]



data=pd.read_csv('covid_19_data.csv')
data1=pd.read_csv('time_series_covid_19_recovered.csv')
data2=pd.read_csv('time_series_covid_19_deaths.csv')
data3=pd.read_csv('time_series_covid_19_confirmed.csv')

new_data3=data3[['4/5/20','Country/Region','Province/State']].sort_values('4/5/20',ascending=False).groupby('Country/Region').sum().sort_values('4/5/20',ascending=False).reset_index()
confirmed=new_data3['4/5/20'].sum()
new_data2=data2[['4/5/20','Country/Region','Province/State']].sort_values('4/5/20',ascending=False).groupby('Country/Region').sum().sort_values('4/5/20',ascending=False).reset_index()
deaths=new_data2['4/5/20'].sum()
new_data1=data1[['4/5/20','Country/Region','Province/State']].sort_values('4/5/20',ascending=False).groupby('Country/Region').sum().sort_values('4/5/20',ascending=False).reset_index()
recovered=new_data1['4/5/20'].sum()
#new_data=data.groupby('Country/Region')['Confirmed'].sum().reset_index()



countrynames=data3.groupby('Country/Region').sum().drop(['Lat','Long'],axis=1)
countrynames1=data2.groupby('Country/Region').sum().drop(['Lat','Long'],axis=1)
countrynames3=data1.groupby('Country/Region').sum().drop(['Lat','Long'],axis=1)
options=[]
for i in countrynames.index:
    options.append({'label':i,'value':i})

#trace1=go.Scatter()






app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout=html.Div([
    html.H1("Corona Virus Pandemic",style={'color':'#fff','text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Confirmed cases",className='text-light'),
                    html.H4(confirmed,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered Cases",className='text-light'),
                    html.H4(recovered,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-4'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths",className='text-light'),
                    html.H4(deaths,className='text-light')
                ],className='card-body')
            ],className='card bg-info')
        ],className='col-md-4')

    ],className='row'),
    html.Div([
        html.H1(style={'padding':'30'})
    ],className='row'),
    html.Div([
        html.Div([

            dcc.Graph(id='map_plot', figure={'data': [go.Choropleth(
                locations=new_data3['Country/Region'],
                locationmode='country names',
                autocolorscale=False,
                colorscale='Blackbody',
                text=new_data3['Country/Region'],
                z=new_data3['4/5/20'],
                marker_line_color='white'


            )], 'layout': go.Layout(title='Affected Countries in the World',
                geo=dict(scope='world')
            )})
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='Albania'),
                    dcc.Graph(id='line')

                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
],className='container')


@app.callback(Output('line','figure'), [Input('picker','value')])
def update_graph(type):
    totalcases=countrynames.loc[type].reset_index()
    deathrate=countrynames1.loc[type].reset_index()
    recoveryrate=countrynames3.loc[type].reset_index()

    trace1=go.Scatter(x=totalcases['index'],y=totalcases[type],mode='lines+markers',marker={'color':'#00a65a'},name='Confirmed Cases')
    trace2=go.Scatter(x=deathrate['index'],y=deathrate[type],mode='lines+markers',marker={'color':'#a60021'},name='Deaths')
    trace3=go.Scatter(x=recoveryrate['index'],y=recoveryrate[type],mode='lines+markers',marker={'color':'#007fa6'},name='Recovered')
    return {'data':[trace1,trace2,trace3],'layout':go.Layout(title='Compartive analysis for countries')}



if __name__=="__main__":
   app.run_server(debug=True)