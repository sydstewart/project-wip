from ._anvil_designer import active_projects_new_column_reportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class active_projects_new_column_report(active_projects_new_column_reportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    boards =list({(r['project_board']) for r in app_tables.projects.search(tables.order_by('project_board'))})
    self.project_board_dropdown.items = boards
    # Any code you write here will run before the form opens.
    dicts_boards =anvil.server.call('active_board_stages')
    print(dicts_boards)
    filter_string= 'API Upgrades'
    dicts ={}
    result =dicts(
                (k,v)
                for k,v in dicts_boards() if filter_string in k)
    # newl = [d for d in dictn if d['project_board'] = filter_string]
    # filtered_dict = dict((d['Name'], d) for d in newl)
    # filter_string = "Maintenance Upgrades, Server Moves, Add on Modules"
    # result= [dicts_boards[i] for i in filter_string if i in dicts_boards]
    print(result)
    k='project_board'
    result = {k:v for k,v in dicts_boards.items if filter_string in k}
    # result = {key:value for (key, value) in dicts_boards.items() if key = "Maintenance Upgrades, Server Moves, Add on Modules"}
    # dicts_boards = {key:value for (key, value) in dicts_boards.items() if value >= 170}
    self.repeating_panel_1.items = result

  def text_area_1_change(self, **event_args):
    """This method is called when the text in this text area is edited"""

    pass

  def project_board_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

