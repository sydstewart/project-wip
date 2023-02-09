from ._anvil_designer import stacked_bar_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stacked_bar_chart(stacked_bar_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    records = app_tables.projects_stages.search(tables.order_by('project_column'), project_column=q.not_('90. Gone Live - Completed','40. Done','Released','Archive','Done','To Archive','To be re-visited','Archived', '10. Completed'))
    print('No of Stages',len(records))
#     dicts = {'project_column' : [],'project_board': [],'count':[], 'new_column': []} 
    for r in records:

      dicts = [{'project_column' : r['project_column'],'project_board': r['project_board'],'count':r['count'], 'new_column': r['new_project_column']['new_column']} for r in records ]

    dicts = sorted(dicts, key=lambda d: d['new_column']) 
#     print(newlist)
    print(dicts)
 
   
    self.plot_1.layout.title= 'Stacked WIP Bar Chart' 


    self.plot_1.data = go.Bar(x=[r['new_column']  for r in dicts] ,
                          y=[r['count'] for r in dicts], barmode = 'stack', color = [r['project_board'] for r in dicts] )
    pass
 
