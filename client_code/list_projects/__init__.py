from ._anvil_designer import list_projectsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from ..tallies import tallies
class list_projects(list_projectsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    

  def percent_complete_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    dicts ,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    tallies(self, dicts)
    pass

  def Category_change(self, **event_args):
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Category =', self.Category.selected_value)
    dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
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