from ._anvil_designer import Tableau_FormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Tableau_Form(Tableau_FormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dicts, number_of_records = anvil.server.call('wipprojects')
    self.label_1.text = number_of_records
    self.repeating_panel_1.items = dicts
    # Any code you write here will run before the form opens.
