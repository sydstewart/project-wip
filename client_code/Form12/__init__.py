from ._anvil_designer import Form12Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from .. new_searches import new_searches


class Form12(Form12Template):
 
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.users.login_with_form()
    # self.data_row_panel_1.item = {'order_no': 'Order No'}
    # self.link_map = {'order_no':self.link_1,
    #                  'order_date': self.link_2,
    #                  'project_name':self.link_3,
    #                  'stage':self.link_4,
    #                  'waiting_on':self.link_5,
    #                  'percent_complete':self.link_6,
    #                  'order_value':self.link_7,
    #                   'assigned_to' :self.link_8,
    #                  'work_to_do':self.link_9,
    #                  'days_elapsed':self.link_10}

    print('Start', datetime.now())



    with Notification("Please wait... data loading "):
      new_searches(self)
      print('end', datetime.now())



    print('end display', datetime.now())
    # Any code you write here will run before the form opens.

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    with Notification("Please wait... data loading "):
      new_searches(self)
      print('end', datetime.now())
      pass



    pass

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    with Notification("Please wait... data loading "):
      self.multi_select_drop_down_1.visible = False
      self.label_18.visible = False
      if self.drop_down_1.selected_value is None:
          self.multi_select_drop_down_1.visible = True  
          self.label_18.visible = True
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
    if self.link_5.icon =='':
      self.link_5.icon ='fa:sort-alpha-desc'
      self.link_11.icon=''
      self.link_10.icon=''
      self.link_6.icon=''
      self.link_8.icon = ''
      self.link_9.icon = ''
      self.link_15.icon = ''
      direction = True
    elif self.link_5.icon =='fa:sort-alpha-desc':
      self.link_5.icon ='fa:sort-alpha-asc'
      direction = False
    elif self.link_5.icon =='fa:sort-alpha-asc':
      self.link_5.icon ='fa:sort-alpha-desc'
      direction = True
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['percent_complete']), reverse=direction ) 
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    # event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    # for a,b in self.link_map.items():
    #   if b ==event_args['sender']:
    #     v=a
    # for l in self.data_row_panel_1.get_components():
    #   if event_args['sender'] is not l:
    #     l.icon=None
    # self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    # self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    # event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    # for a,b in self.link_map.items():
    #   if b ==event_args['sender']:
    #     v=a
    # for l in self.data_row_panel_1.get_components():
    #   if event_args['sender'] is not l:
    #     l.icon=None
    # self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    # self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    # event_args['sender'].icon='fa:caret-up' if event_args['sender'].icon=='fa:caret-down' else 'fa:caret-down'
    # for a,b in self.link_map.items():
    #   if b ==event_args['sender']:
    #     v=a
    # for l in self.data_row_panel_1.get_components():
    #   if event_args['sender'] is not l:
    #     l.icon=None
    # self.repeating_panel_1.items = sorted(self.repeating_panel_1.items, key=lambda k: k[v], reverse=event_args['sender'].icon=='fa:caret-up')
    # self.repeating_panel_1.items=self.repeating_panel_1.items
    pass

  def link_6_click(self, **event_args):
    if self.link_6.icon =='':
      self.link_6.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_10.icon = ''
      self.link_11.icon = ''
      self.link_8.icon = ''
      self.link_9.icon = ''
      self.link_15.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_value']), reverse=direction ) 
    elif self.link_6.icon =='fa:sort-alpha-desc':
      self.link_6.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_value']), reverse=direction ) 
    elif self.link_6.icon =='fa:sort-alpha-asc':
      self.link_6.icon ='fa:sort-alpha-desc'
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_value']), reverse=direction ) 

      pass

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""

    if self.link_10.icon =='':
      self.link_10.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_11.icon = ''
      self.link_6.icon = ''
      self.link_8.icon = ''
      self.link_9.icon = ''
      self.link_15.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_date']), reverse=direction ) 
    elif self.link_10.icon =='fa:sort-alpha-desc':
      self.link_10.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_date']), reverse=direction ) 
    elif self.link_10.icon =='fa:sort-alpha-asc':
      self.link_10.icon ='fa:sort-alpha-desc'
      direction = True
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_date']), reverse=direction ) 
    pass

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_11.icon =='':
      self.link_11.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_6.icon = ''
      self.link_10.icon = ''
      self.link_8.icon = ''
      self.link_9.icon = ''
      self.link_15.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_no']), reverse=direction ) 
    elif self.link_11.icon =='fa:sort-alpha-desc':
      self.link_11.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_no']), reverse=direction ) 
    elif self.link_11.icon =='fa:sort-alpha-asc':
      self.link_11.icon ='fa:sort-alpha-desc'
      direction = True
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_no']), reverse=direction ) 
    pass
    pass

  def category_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    new_searches(self)
    print('end', datetime.now())
    pass

  def app_area_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    new_searches(self)
    print('end', datetime.now())
    pass

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_8.icon =='':
      self.link_8.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_10.icon = ''
      self.link_11.icon = ''
      self.link_9.icon = ''
      self.link_15.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['work_to_do']), reverse=direction ) 
    elif self.link_8.icon =='fa:sort-alpha-desc':
      self.link_8.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['work_to_do']), reverse=direction ) 
    elif self.link_8.icon =='fa:sort-alpha-asc':
      self.link_8.icon ='fa:sort-alpha-desc'
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['work_to_do']), reverse=direction ) 

    pass

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_9.icon =='':
      self.link_9.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_10.icon = ''
      self.link_11.icon = ''
      self.link_8.icon = ''
      self.link_15.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['days_elapsed']), reverse=direction ) 
    elif self.link_9.icon =='fa:sort-alpha-desc':
      self.link_9.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['days_elapsed']), reverse=direction ) 
    elif self.link_9.icon =='fa:sort-alpha-asc':
      self.link_9.icon ='fa:sort-alpha-desc'
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['days_elapsed']), reverse=direction ) 
    pass

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_11.icon =='':
      self.link_11.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_6.icon = ''
      self.link_10.icon = ''
      self.link_8.icon = ''
      self.link_9.icon = ''
      self.link_15.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_no']), reverse=direction ) 
    elif self.link_11.icon =='fa:sort-alpha-desc':
      self.link_11.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_no']), reverse=direction ) 
    elif self.link_11.icon =='fa:sort-alpha-asc':
      self.link_11.icon ='fa:sort-alpha-desc'
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['order_no']), reverse=direction ) 
    pass
        


  def link_14_click(self, **event_args):
      """This method is called when the link is clicked"""
      self.text_box_1.text =''
      self.drop_down_1.selected_value = None
      self.drop_down_2.selected_value = None
      self.drop_down_3.selected_value = None
      self.app_area_drop_down.selected_value = None
      self.category_drop_down.selected_value = None
      self.multi_select_drop_down_1.selected = None
      if not self.multi_select_drop_down_1.selected :
        self.drop_down_1.visible = True
        self.label_3.visible = True
      if self.drop_down_1.selected_value is None:
          self.multi_select_drop_down_1.visible = True  
          self.label_18.visible = True
      new_searches(self)
      pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    # self.column_panel_1.clear()

    anvil.users.logout()

    anvil.users.login_with_form()
    open_form('Testquery')
    pass

  def link_15_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.link_15.icon =='':
      self.link_15.icon ='fa:sort-alpha-desc'
      self.link_5.icon = ''
      self.link_10.icon = ''
      self.link_11.icon = ''
      self.link_8.icon = ''
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['partially_invoiced_total']), reverse=direction ) 
    elif self.link_15.icon =='fa:sort-alpha-desc':
      self.link_15.icon ='fa:sort-alpha-asc'
      direction = False
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['partially_invoiced_total']), reverse=direction ) 
    elif self.link_15.icon =='fa:sort-alpha-asc':
      self.link_15.icon ='fa:sort-alpha-desc'
      direction = True
      self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['partially_invoiced_total']), reverse=direction ) 
      pass

  def radio_button_1_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    with Notification("Please wait... data loading "):
      new_searches(self)
      
      # orders = anvil.server.call('orders',self.text_box_1.text,self.drop_down_1.selected_value)
      # self.repeating_panel_1.items = orderspass

  def multi_select_drop_down_1_change(self, **event_args):
    """This method is called when the selected values change"""
    self.drop_down_1.visible = False
    self.label_3.visible = False
    if not self.multi_select_drop_down_1.selected :
      self.drop_down_1.visible = True
      self.label_3.visible = True
    new_searches(self)
    pass

