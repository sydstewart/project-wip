import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
@anvil.server.callable
def bar_charts(dicts):
#   barcharts = pd.DataFrame()
#   records = app_tables.projects_stages.search(tables.order_by('project_column'),project_board= board)
   
#   for r in records:
#           dicts = [{'project_column' : r['project_column'],'project_board': r['project_board'],'count':r['count'], 'new_column': new_column['new_column']} for r in records]

      df = pd.DataFrame.from_dict(dicts)
      df.sort_values(by= 'new_column', inplace=True)
#   df = df.groupby('project_board').sum()
#   barchart = go.Bar( 
#             x=df['new_column'] ,
#             y=df['count'],
#             )
# #             color = df[ 'project_board'])
# #             mark_color = df['project_board'])             
# #   x=dfg['name'], y=dfg['%']) for group, dfg in df.groupby(by='week')]          
#   return barchart
       
      fig = px.bar( df, x=df['new_column'] , y= df['count'] , color =df['project_board'] ,title="Project Stages")
      return fig 