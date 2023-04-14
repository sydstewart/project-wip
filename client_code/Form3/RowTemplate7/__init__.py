from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
   
    print('Project board of line', self.item['project_board'])
    result = alert(content=Form2_copy(self.item['project_board'], self.item['new_column']), title="Projects", buttons=[], large=True)
    pass


