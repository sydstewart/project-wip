from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from ..Module3 import background_check_tick
from ..Form3 import Form3
from ..Form4 import Form4
from ..Form5 import Form5
from ..active_projects_report import active_projects_report

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_type = anvil.users.get_user()['user_type'] 
    if user_type == 'admin':
      self.refresh_date_button.visible = True
      self.restore_stage_translate_button.visible = True
    # Any code you write here will run before the form opens.

  def Logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    anvil.users.logout()

    anvil.users.login_with_form()
    # global user_type
    # user_type = anvil.users.get_user()['user_type']
    
    open_form('Main')

    pass
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts_stages = anvil.server.call('groupby_new_column')
    open_form('Form3')

  def stacked__click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stacked_bar_chart')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dev_board_form')
    pass

  def refresh_date_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    # background_check_tick(self)
    # with Notification("Please wait..."):
    anvil.server.call('load_data')
    # state = self.task.get_state()
    # print(state)
    t = app_tables.last_date_refreshed.get(date_id =1 )
    t['last_date_refreshed'] = str(datetime.today() )
    pass

  def active_projects_report_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(active_projects_report(), full_width_row=True)
    pass



  def active_projects_by_stage_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form3(), full_width_row=True)
    pass
 
  def search_projects_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Form4(), full_width_row=True)
    pass

  def restore_stage_translate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Restore')
    pass












def Logout_click(self, **event_args):
  """This method is called when the button is clicked"""
  self.content_panel.clear()
  self.column_panel_1.clear()
  anvil.users.logout()

  anvil.users.login_with_form()
  open_form('home')



  pass
