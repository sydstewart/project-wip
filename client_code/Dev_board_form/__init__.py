from ._anvil_designer import Dev_board_formTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Dev_board_form(Dev_board_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    boards =list({(r['project_board']) for r in app_tables.projects_stages.search(tables.order_by('project_board'))})
    self.board_dropdown.items = boards
    records = app_tables.projects_stages.search(tables.order_by('project_column'),project_board= self.board_dropdown.selected_value)
#     self.plot_1.layout.title= self.board_dropdown.selected_value
#     self.plot_1.data = go.Bar(x=[r['project_column'] for r in records],
#                               y=[r['count'] for r in records])
    

  def board_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""

    records = app_tables.projects_stages.search(tables.order_by('project_column'),project_board= self.board_dropdown.selected_value, project_column=q.not_('90. Gone Live - Completed','40. Done','Released','Archive','Done','To Archive','To be re-visited','Archived'))
    print('No of Stages',len(records))
    # print('records=',records['project_board'])
#     dicts = {'project_column' : [],'project_board': [],'count':[], 'new_column': []} 
    for r in records:

      dicts = [{'project_column' : r['project_column'],'project_board': r['project_board'],'count':r['count'], 'new_column': r['new_project_column']['new_column'] }  for r in records] #'days_work': r['no_of_days_work'], 'total': r['count']*r['no_of_days_work'],'old_column': r['new_project_column']['project_column'] }  for r in records]
      
    dicts = sorted(dicts, key=lambda d: d['new_column']) 
#     print(newlist)
    print(dicts)
 


    
    self.plot_1.layout.title= self.board_dropdown.selected_value


    self.plot_1.data = go.Bar(x=[r['new_column']  for r in dicts],
                          y=[r['count']  for r  in dicts], color = r['project_column'],barmode='group')
 
    pass
    self.repeating_panel_1.items = dicts
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('home')
    pass

 
def stacked_board_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""

    records = app_tables.projects_stages.search(tables.order_by('project_column'),project_board= self.board_dropdown.selected_value, project_column=q.not_('90. Gone Live - Completed','40. Done','Released','Archive','Done','To Archive','To be re-visited','Archived'))
    print('No of Stages',len(records))
#     dicts = {'project_column' : [],'project_board': [],'count':[], 'new_column': []} 
    for r in records:

      dicts = [{'project_column' : r['project_column'],'project_board': r['project_board'],'count':r['count'], 'new_column': r['new_project_column']['new_column']} for r in records ]

    dicts = sorted(dicts, key=lambda d: d['new_column']) 
#     print(newlist)
    print(dicts)
 


    
    self.plot_1.layout.title= self.board_dropdown.selected_value


    self.plot_1.data = go.Bar(x=[r['new_column']  for r in dicts] ,
                          y=[r['total'] for r in dicts] )
    pass