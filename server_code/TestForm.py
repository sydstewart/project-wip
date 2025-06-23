import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pymysql
import anvil.tables.query as q
import anvil.media
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, time, date, timedelta
import numpy as np

@anvil.server.callable
def testform():
  import plotly.graph_objects as go
  import plotly.express as px 
  chart_data = app_tables.daily_wip.search(tables.order_by("Date_of_WIP", ascending=False) ,Date_of_WIP= q.greater_than(date(year=2024, month=7, day=17)))
  dicts = [{'Date_entered': r['Date_of_WIP'], 'Total Order Value': r['Total_Order_Value'], 'Total Work To Do Value': r['Total_Work_To_Do_Value']} for r in chart_data]
  df = pd.DataFrame.from_dict(dicts)
  print('df',df)


  fig = go.Figure([

    go.Scatter(
      name='Total Work To Do Value',
      x=df['Date_entered'],
      y=df['Total Work To Do Value'],
      mode='lines+markers',
      marker=dict(color='blue', size=4),
      line=dict(width=1),
      showlegend=True)
  ])
  fig.update_layout(
    title=dict(
      text='Run Chart of Sales Opportunity Count per Week' + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    ),
    yaxis=dict(
      title=dict(
        text="Opportunity Count"
      )
    ),
    xaxis=dict(
      title=dict(
        text="Week Start Date"
      )  
    ))
  fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.90
  ))
  fig.update_traces(marker_size=10)
  return fig
