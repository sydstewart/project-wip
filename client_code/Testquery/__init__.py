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
    self.data_row_panel_1.item = {'order_no': 'Order No'}
    self.link_map = {'order_no':self.link_1,
                     'order_date': self.link_2,
                     'project_name':self.link_3,
                     'stage':self.link_4,
                     'waiting_on':self.link_5,
                     'percent_complete':self.link_6,
                     'order_value':self.link_7,
                      'assigned_to' :self.link_8,
                     'work_to_do':self.link_9,
                     'days_elapsed':self.link_10}
    
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

  def drop_down_3_change(self, **event_args):
    """This method is called when an item is selected"""
    new_searches(self)
    # orders = anvil.server.call('orders',self.text_box_1.text,self.drop_down_1.selected_value)
    # self.repeating_panel_1.items = orders
    print('end', datetime.now())
    pass
    pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    for a,b in self.link_map.items():
      if b ==event_args['sender']:
        v=a
    for l in self.data_row_panel_1.get_components():
      if event_args['sender'] is not l:
        l.icon=None
    self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    self.repeating_panel_1.items=self.repeating_panel_1.items

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    for a,b in self.link_map.items():
      if b ==event_args['sender']:
        v=a
    for l in self.data_row_panel_1.get_components():
      if event_args['sender'] is not l:
        l.icon=None
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['percent_complete']), reverse=True )
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    for a,b in self.link_map.items():
      if b ==event_args['sender']:
        v=a
    for l in self.data_row_panel_1.get_components():
      if event_args['sender'] is not l:
        l.icon=None
    self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    for a,b in self.link_map.items():
      if b ==event_args['sender']:
        v=a
    for l in self.data_row_panel_1.get_components():
      if event_args['sender'] is not l:
        l.icon=None
    self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    for a,b in self.link_map.items():
      if b ==event_args['sender']:
        v=a
    for l in self.data_row_panel_1.get_components():
      if event_args['sender'] is not l:
        l.icon=None
    self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    for a,b in self.link_map.items():
      if b ==event_args['sender']:
        v=a
    for l in self.data_row_panel_1.get_components():
      if event_args['sender'] is not l:
        l.icon=None
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_value']), reverse=event_args['sender'].icon=='fa:caret-up' )

    # self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  