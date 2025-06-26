import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
from datetime import datetime, time, date, timedelta

@anvil.server.callable
def piechart():

  last_row = app_tables.stage_summary.search(tables.order_by('Date_of_WIP', ascending=False))[0]
  dicts_pie = dict(last_row)
  import plotly.graph_objects as go
  colors = ['gold', 'mediumturquoise', 'lightgreen' ]
  labels = ['On Hold','In_Progress','Waiting_to_Start']
  values = [ dicts_pie['Sum_on_hold'], dicts_pie['Sum_in_Progress'], dicts_pie['Sum_in_Waiting_to_Start']]
                                      
  fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
  fig.update_layout(
    title=dict(
      text='Pie Chart of Stage Groups GBP Excl VAT' + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    ))
  fig.update_traces(hoverinfo='label+percent', textinfo='value +percent', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
  
  return dicts_pie, fig
 
  