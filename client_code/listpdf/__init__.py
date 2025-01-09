from ._anvil_designer import listpdfTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class listpdf(listpdfTemplate):
  def __init__(self, dicts, field_parameters,  **properties):
    # Set Form properties and Data Bindings.
    print(dicts)
    self.init_components(**properties)
    self.repeating_panel_1.items = dicts
    self.assigned_to_label.text = field_parameters[0]
    self.no_of_projects_label.text =  f"No of Projects : {field_parameters[1]}"
    self.category_label.text =   f"Category : {field_parameters[2]}" 
    self.above_percent_complete_label.text =   f"Percent Complete : {field_parameters[3]}" 
    self.average_completion_label.text = field_parameters[4]
    self.total_value_label.text =field_parameters[5]
    self.work_to_do_label.text = field_parameters[6]
    self.assigned_to_label.text =   f"Assign_To : {field_parameters[0]}"


    # Any code you write here will run before the form opens.
