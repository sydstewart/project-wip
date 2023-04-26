from ._anvil_designer import active_projects_list_by_stageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class active_projects_list_by_stage(active_projects_list_by_stageTemplate):
  def __init__(self, new_column, **properties):

     
    print('new_column=' + new_column)
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    boards =list({(r['project_board']) for r in app_tables.projects.search(tables.order_by('project_board'))})
    self.multi_select_board_drop_down.items = boards
    project_stages = app_tables.stage_translate.search(new_column = new_column)
    thislist =[]
    for row in project_stages:
        thislist.append(row['project_column'])
      
    self.repeating_panel_1.items = app_tables.projects.search(project_column = q.any_of(*thislist))

  def multi_select_board_drop_down_change(self, **event_args):
    """This method is called when the selected values change"""
    project_stages = app_tables.stage_translate.search(new_column = new_column)
    thislist =[]
    for row in project_stages:
        thislist.append(row['project_column'])
    self.repeating_panel_1.items = app_tables.projects.search(project_column = q.any_of(*thislist), project_board= self.multi_select_board_drop_down.selected)
    pass


                                                                        
