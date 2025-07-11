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
from ..stage_group_new_chart import stage_group_new_chart
from ..projects_in_progress_new import projects_in_progress_new
from ..projects_waiting_to_start_new import projects_waiting_to_start_new
from ..projects_on_hold_new import projects_on_hold_new

# def reset_links():
#   self.link_7.role = ''
#   # self.link_1.role = None
#   # self.link_2.role = None
#   # self.link_3.role = None
#   # self.link_4.role = None
#   # self.link_5.role = None
#   # self.link_6.role = None
#   pass
  
class Form9(Form9Template):
  def __init__(self, **properties):
    # def reset_links(self, **event_args):
    #   self.link_3.role = ''
    #   self.link_2.role = ''
    #   self.link_1.role = ''
    #   self.link_2.role = ''
    #   self.link_3.role = ''
    #   self.link_4.role = ''
    #   self.link_5.role = ''
    #   self.link_6.role = ''
    #   self.link_7.role =''
    #   pass
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_5_click()

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

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(stage_group_new_chart(), full_width_row=True)
    pass

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(projects_in_progress_new(), full_width_row=True)
    pass

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(projects_waiting_to_start_new(), full_width_row=True)
    pass

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.reset_links()
    self.link_7.role ='Selected'

    
    self.content_panel.add_component(projects_on_hold_new(), full_width_row=True)
    pass


