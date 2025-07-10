from ._anvil_designer import projects_in_progress_newTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.tz

class projects_in_progress_new(projects_in_progress_newTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    a = "Projects in Progress at" 
    b = (datetime.now().strftime("%Y-%m-%d"))
    self.label_1.text = a + " " + b
    
    # dicts,Xmedia  = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    dicts, dictspip, Xmedia,pivotsyd_to_markdown  = anvil.server.call('get_orders_for_pivots', 0, 100, None, None, None)
    
    self.repeating_panel_1.items = dictspip
    order_total = (sum(item['order_value'] 
                               for item in self.repeating_panel_1.items))
    order_total= str('£' + str(round(order_total,0)))

    days_elapsed_sum = (sum(item['days_elapsed'] 
                       for item in self.repeating_panel_1.items))
    days_elapsed_average= (round(days_elapsed_sum))/len(self.repeating_panel_1.items)
    days_elapsed_average= str(round(days_elapsed_average)) 
    
    self.repeating_panel_1.items.append({'order_value_formated': order_total, 'days_elapsed':'<b>' +days_elapsed_average + '</b>' })
    self.repeating_panel_1.items = self.repeating_panel_1.items
    # Any code you write here will run before the form opens.


  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_2.checked = False
    self.check_box_3.checked = False
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['percent_complete']), reverse=True )
    pass

  def check_box_2_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_1.checked = False
    self.check_box_3.checked = False
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['Value yet to be invoiced']), reverse=True )
    pass

  
  def check_box_3_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_1.checked = False
    self.check_box_2.checked = False
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['days_elapsed']), reverse=True )
    pass
    
