from ._anvil_designer import list_projectsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from ..tallies import tallies
from..sorting import set_sorting

class list_projects(list_projectsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    dicts, Xmedia ,pivotsyd = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value, self.filter.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    # self.rich_text_1.content = pivotsyd
    
    # self.pivot_1.items=dicts
    # self.plot_1.figure= pivotsyd

  def percent_complete_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    dicts,Xmedia , pivots = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value, self.filter.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    
    

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    print('Invoiced not complete' ,self.filter.selected_value)
    dicts ,Xmedia, pivots = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value, self.filter.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    pass

  def Category_change(self, **event_args):
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Category =', self.Category.selected_value)
    print('Invoiced not complete' ,self.filter.selected_value)
    if self.check_box_1.enabled:
       bool_value = True
    dicts,Xmedia, pivots = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value, self.filter.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    
    pass

  def download_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # start = self.level_textbox.text
    field_parameters =[]
    field_parameters = [self.drop_down_1.selected_value,  #asigned to
                        self.text_box_1.text, # no of records
                        self.Category.selected_value,  # category
                        self.percent_complete_text_box.text,  # above this percent complete
                        self.average_completion_label.text, #above percent 
                        self.work_to_do_label.text, # work to do
                        self.total_value_label.text]
                       
    
    # open_form('listpdf',self.repeating_panel_1.items, field_parameters )
    pdf = anvil.server.call('create_pdf', self.repeating_panel_1.items,field_parameters)
    download(pdf)

  def Pivots_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts, Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    open_form('pivots', dicts)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    download(Xmedia)    

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Work_in_Progress')
    pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    object_name = self.link_1 #Link name
    column_name = 'percent_complete'#real name in database
    set_sorting(self,object_name, column_name)
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    object_name = self.link_3 #Link name
    column_name = 'order_value'#real name in database
    set_sorting(self,object_name, column_name)
    pass

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    object_name = self.link_8 #Link name
    column_name = 'order_date'#real name in database
    set_sorting(self,object_name, column_name)
    pass
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    object_name = self.link_4 #Link name
    column_name = 'days_elapsed'#real name in database
    set_sorting(self,object_name, column_name)
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    object_name = self.link_5 #Link name
    column_name = 'partially_invoiced_total'#real name in database
    set_sorting(self,object_name, column_name)
    pass

  def percent_complete_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Category =', self.Category.selected_value)
    print('Invoiced not complete' ,self.check_box_1.checked)
    dicts,Xmedia, pivots = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value, self.filter.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    pass

  def filter_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Category =', self.Category.selected_value)
    print('Invoiced not complete' ,self.filter.selected_value)
    dicts,Xmedia, pivots = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value, self.filter.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    pass
