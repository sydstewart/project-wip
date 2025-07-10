from ._anvil_designer import Form9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..pie_charts_new import pie_charts_new
from ..pivots_new import pivots_new
from ..Run_Chart_New import Run_Chart_New

class Form9(Form9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_3_click()
    
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    # self.reset_links()
    # self.link_1.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(pie_charts_new(), full_width_row=True)
    # self.reset_links()
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""

    self.content_panel.clear()
    self.content_panel.add_component(pivots_new(), full_width_row=True)
    # self.reset_links()
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Run_Chart_New(), full_width_row=True)
    # self.reset_links()
    pass
 
