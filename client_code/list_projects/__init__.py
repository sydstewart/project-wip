from ._anvil_designer import list_projectsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from ..kwargs_for_projects import search_projects_using_kwargs

class list_projects(list_projectsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Catgeory =', self.Category.selected_value)
    kwargs ={X['assigned_to']}
    if self.drop_down_1.selected_value:
      
    dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    # fract_to_do = dicts['percent_complete']/100
    # print('Fract to do =', fract_to_do)
    # average_completion = average([int(x['percent_complete'])] for x in dicts]))
    average_completion = sum([int(x['percent_complete']) / len(dicts)  for x in dicts])
    subtotal = sum([int(x['order_value'] ) for x in dicts])
    work_to_do = (subtotal * (100 - average_completion))/ 100
    self.total_value_label.text = f"TOTAL_VALUE_TO_DO : £{subtotal:,}"
    self.average_completion_label.text = f"Average_COMPLETION : {average_completion:.1f}%"
    self.work_to_do_label.text = f"Value_of_Work_TO_DO : £{work_to_do:,}"

  def percent_complete_text_box_change(self, **event_args):
    
    """This method is called when the text in this text box is edited"""
    search_projects_using_kwargs(self)
    # print('Percent Complete=', self.percent_complete_text_box.text)
    # print('Assigned to =', self.drop_down_1.selected_value)
    # print('Catgeory =', self.Category.selected_value)
    # dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    # self.text_box_1.text = len(dicts)
    # self.repeating_panel_1.items = dicts
    # average_completion = sum([int(x['percent_complete']) / len(dicts)  for x in dicts])
    # subtotal = sum([int(x['order_value'] ) for x in dicts])
    # work_to_do = (subtotal * (100 - average_completion))/ 100
    # self.total_value_label.text = f"TOTAL_VALUE_TO_DO : £{subtotal:,}"
    # self.average_completion_label.text = f"Average_COMPLETION : {average_completion:.1f}%"
    # self.work_to_do_label.text = f"Value_of_Work_TO_DO : £{work_to_do:,}"

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    search_projects_using_kwargs(self)
    # print('Percent Complete=', self.percent_complete_text_box.text)
    # print('Assigned to =', self.drop_down_1.selected_value)
    # print('Catgeory =', self.Category.selected_value)
    # dicts ,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    # self.text_box_1.text = len(dicts)
    # self.repeating_panel_1.items = dicts
    # average_completion = sum([int(x['percent_complete']) / len(dicts)  for x in dicts])
    # subtotal = sum([int(x['order_value'] ) for x in dicts])
    # work_to_do = (subtotal * (100 - average_completion))/ 100
    # self.total_value_label.text = f"TOTAL_VALUE_TO_DO : £{subtotal:,}"
    # self.average_completion_label.text = f"Average_COMPLETION : {average_completion:.1f}%"
    # self.work_to_do_label.text = f"Value_of_Work_TO_DO : £{work_to_do:,}"
    pass

  def Category_change(self, **event_args):
    """This method is called when an item is selected"""
    print('Percent Complete=', self.percent_complete_text_box.text)
    print('Assigned to =', self.drop_down_1.selected_value)
    print('Category =', self.Category.selected_value)
    dicts,Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    average_completion = sum([int(x['percent_complete']) / len(dicts)  for x in dicts])
    subtotal = sum([int(x['order_value'] ) for x in dicts])
    work_to_do = (subtotal * (100 - average_completion))/ 100
    self.total_value_label.text = f"TOTAL_VALUE_TO_DO : £{subtotal:,}"
    self.average_completion_label.text = f"Average_COMPLETION : {average_completion:.1f}%"
    self.work_to_do_label.text = f"Value_of_Work_TO_DO : £{work_to_do:,}"
    pass

  def download_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # start = self.level_textbox.text
    open_form('list_projects_pdf',self.repeating_panel_1.items )
    pdf = anvil.server.call('create_pdf', self.repeating_panel_1.items)
    download(pdf)
    