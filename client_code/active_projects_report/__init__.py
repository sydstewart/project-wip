from ._anvil_designer import active_projects_reportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class active_projects_report(active_projects_reportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    dicts_boards =anvil.server.call('active_projects')
    self.repeating_panel_1.items = dicts_boards
