from ._anvil_designer import TestProjectTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TestProject(TestProjectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

        # Set Form properties and Data Bindings.
    self.init_components(**properties)
    records,totals, number_of_records = anvil.server.call('testprojects')
    self.text_box_1.text = number_of_records
    for r in totals:
      print('Total_Order_Value1=',r['Total_Order_Value'])
      print('Average_WIP1=',r['Average_WIP'])
      print('Total_WIP_VaLUE1',r['Total_WIP_VaLUE'])
      self.text_box_2.text = r['Total_Order_Value']
    self.repeating_panel_1.items = records
    self.repeating_panel_2.items =totals
    # Any code you write here will run before the form opens.
