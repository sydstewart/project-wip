from ._anvil_designer import TestqueryTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from .. new_searches import new_searches


class Testquery(TestqueryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Start', datetime.now())
 
    
    
    with Notification("Please wait... data loading "):
        new_searches(self)
        # orders = anvil.server.call('orders',**kwargs)
        # self.repeating_panel_1.items = orders
        print('end', datetime.now())
        # self.repeating_panel_1.items = orders
        
     
    print('end display', datetime.now())
    # Any code you write here will run before the form opens.

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    with Notification("Please wait... data loading "):
      new_searches(self)
      # orders = anvil.server.call('orders',**kwargs)
      # self.repeating_panel_1.items = orders
      print('end', datetime.now())
      # self.repeating_panel_1.items = orders
      
    
    
    pass

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    with Notification("Please wait... data loading "):
      new_searches(self)
      # orders = anvil.server.call('orders',self.text_box_1.text,self.drop_down_1.selected_value)
      # self.repeating_panel_1.items = orders
      print('end', datetime.now())
      # self.repeating_panel_1.items = orders
     
    pass

  def drop_down_2_change(self, **event_args):
    """This method is called when an item is selected"""
    with Notification("Please wait... data loading "):
      new_searches(self)
      # orders = anvil.server.call('orders',self.text_box_1.text,self.drop_down_1.selected_value)
      # self.repeating_panel_1.items = orders
      print('end', datetime.now())
    pass

  