from ._anvil_designer import pivotsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
 

class pivots(pivotsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # dicts,Xmedia  = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    dicts,Xmedia,pivotsyd_to_markdown  = anvil.server.call('get_orders_for_pivots', 0, 100, None, None, None)
    # dicts, Xmedia = anvil.server.call('get_orders', 0,None, None)
    # pivots = anvil.server.call('pivots', dicts)
    print(pivots)
    
    self.pivot_1.rendererOptions = 'Table Barchart'
    
    self.pivot_1.items = dicts
    # self.pivot_1.rows = 'assigned_to'
    # self.pivot_1.rows =['stage']
    # self.pivot_1.rendererOptions.rows= ['stage']
    # self.pivot_1.columns = ['order_category', 'project_name']
    # self
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Work_in_Progress')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    pdf = anvil.server.call('create_pivot_pdf')
    anvil.media.download(pdf)
    pass
