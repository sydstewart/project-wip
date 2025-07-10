from ._anvil_designer import Form9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import pie_charts_new

class Form9(Form9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
   
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('pie_charts_new')
    
    pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    # self.reset_links()
    # self.link_1.role = 'selected'

    self.content_panel.clear()
    self.content_panel.add_component(pie_charts_new(), full_width_row=True)
    # self.reset_links()
    pass
