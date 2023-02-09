import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
import plotly.graph_objects as go

@anvil.server.callable
def bar_charts(dicts):
#   barcharts = pd.DataFrame()
#   records = app_tables.projects_stages.search(tables.order_by('project_column'),project_board= board)
   
#   for r in records:
#           dicts = [{'project_column' : r['project_column'],'project_board': r['project_board'],'count':r['count'], 'new_column': new_column['new_column']} for r in records]

  df = pd.DataFrame.from_dict(dicts)
  barchart = go.Bar(  # x=df[pointdate],
            # y=df[pointname],
            x=df['new_column'],
            y=df['count'],
             
            name='4 out 5 above upper one SD')
  return barchart