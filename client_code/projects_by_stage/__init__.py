from ._anvil_designer import projects_by_stageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class projects_by_stage(projects_by_stageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    dicts_stages =anvil.server.call('groupby_new_column')
    self.repeating_panel_1.items = dicts_stages
  