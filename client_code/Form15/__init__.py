from ._anvil_designer import Form15Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..new_searches_percent import new_searches_percent

class Form15(Form15Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    new_searches_percent(self)
    dicts = anvil.server.call('get_changes')
    print('Number of Record=', len(dicts))
    self.repeating_panel_1.items = dicts
    self.repeating_panel_1.items = sorted(
      self.repeating_panel_1.items,
      key=lambda row: row["Update_Date"],
      reverse=True,
    )

  #   last_date = anvil.server.call('last_import_date')
  #   day_of_week =last_date.strftime("%A")
  #   self.label_2.text = 'Date of Last Import from the CRM = ' + str(last_date) + ' ' + str(day_of_week)
  # # initializing dictionary

  # # printing original dictionary
  #     print("The original dictionary : " + str(dicts))

  #   # initializing K
  #     K = 5

  #   # Filter and Double keys greater than K
  #   # Using loop
  #     dict_list =[dicts]

  # # Use list comprehension to filter the list based on roles
  #     res = [d for d in dict_list if d['Percent Completion Before'] > 10] 
  #     # printing result
  #     print("The filtered dictionary : " + str(res))

    # anvil.media.download(Y)
    # Any code you write here will run before the form opens.

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""

    if self.check_box_1.checked:
      self.repeating_panel_1.items = sorted(
        self.repeating_panel_1.items,
        key=lambda row: row["Update_Date"],
        reverse=True,
      )

    else:
      dicts, XMedia = anvil.server.call('get_changes')
      self.repeating_panel_1.items = dicts

  # def button_1_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.media.download(csv_file)
  #   pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    start = self.level_textbox.text
    dicts , Xmedia = anvil.server.call('get_changes', start)
    download(Xmedia)
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Work_in_Progress')
    pass

  def check_box_2_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    start = self.level_textbox.text
    dicts , Xmedia = anvil.server.call('get_changes', start)

  def level_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    start = self.level_textbox.text
    print('start=',start)
    dicts , Xmedia = anvil.server.call('get_changes', start)
