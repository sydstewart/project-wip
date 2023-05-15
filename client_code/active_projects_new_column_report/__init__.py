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
    dicts_boards=sorted(dicts_boards, key = lambda i: (i['project_board'], i['new_column']))
    # dicts_boards = {key:value for (key, value) in dicts_boards.items() if value >= 170}
    self.repeating_panel_1.items = dicts_boards

  def text_area_1_change(self, **event_args):
    """This method is called when the text in this text area is edited"""

    pass

  def project_board_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    dicts_boards =anvil.server.call('active_board_stages')
    dicts_boards=sorted(dicts_boards, key = lambda i: (i['project_board'], i['new_column']))
    self.repeating_panel_1.items = dicts_boards
    pass

