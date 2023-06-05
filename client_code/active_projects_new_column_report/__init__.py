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
    k = 'project_boards'
    filter_string= 'API Upgrades'
    res = []
    d={}
    key: value for key, value in d1.items() if value > 0}
    for k,v in dicts_boards.items():
       if v = filter_string:
       res[k]=v
