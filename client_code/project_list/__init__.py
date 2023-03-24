from ._anvil_designer import project_listTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class project_list(project_listTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
   self.init_components(**properties)
   self.repeating_panel_1.items = app_tables.projects.search()

  def project_name_searchbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.repeating_panel_1.items = app_tables.projects.search(project_name = q.like('%'  + self.project_name_searchbox.text + '%'))
    pass
