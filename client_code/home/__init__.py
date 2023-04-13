from ._anvil_designer import homeTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Searches import search_using_kwargs 
from ..Module1  import show_projects
from datetime import datetime, time , date , timedelta

class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
# Login
    anvil.users.login_with_form()
    global loggedinuser
    loggedinuser =  anvil.users.get_user()['email']
#     self.loggedinuser.text = loggedinuser
    print('User=',loggedinuser)
    
    user_type = anvil.users.get_user()['user_type']
    # Any code you write here will run before the form opens.
#     self.project_stages_count_textbox.text = len(app_tables.projects_stages.search())
    stages =list({(r['project_column']) for r in app_tables.projects_stages.search(tables.order_by('project_column'))})
    self.multi_select_stage_dropdown.items =stages
    boards =list({(r['project_board']) for r in app_tables.projects_stages.search(tables.order_by('project_board'))})
    self.boards_dropdown.items = boards
 
    rows = app_tables.projects_stages.search(tables.order_by('project_column'))
    rows = [dict(x) for x in rows]
    self.repeating_panel_1.items = rows
    
    self.exclude_completed_checkbox.checked =  True
 
    search_using_kwargs(self)
 #Last Refresh of Data   
    t = app_tables.last_date_refreshed.get(date_id =1 )
    self.last_refresh_date.text= t['last_date_refreshed']

  def refresh_date_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    with Notification("Please wait..."):
       anvil.server.call('load_data')
    alert(' Refresh Completed')
    self.last_refresh_date.text= str(datetime.today()) 
    t = app_tables.last_date_refreshed.get(date_id =1 )
    t['last_date_refreshed'] = str(datetime.today() )
    pass

  def boards_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def multi_select_stage_dropdown_change(self, **event_args):
    """This method is called when the selected values change"""
    search_using_kwargs(self)
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dev_board_form')
    pass

  def stages_translate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    stages =list({(r['project_column']) for r in app_tables.projects_stages.search(tables.order_by('project_column'))})

    for r in stages: 
        dicts = [{'project_column' : r}]
        for d in dicts:
              app_tables.stage_translate.add_row( **d)

  def stacked__click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stacked_bar_chart')
    pass

  def no_of_projects_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def exclude_completed_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    search_using_kwargs(self)
    pass

  def project_count_sort_chkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    search_using_kwargs(self)
    pass

  def project_list_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('project_list')
    pass

  def Logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.column_panel_1.clear()
    anvil.users.logout()
    
    anvil.users.login_with_form()
    open_form('home') 
    
    
    
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts_stages = anvil.server.call('groupby_new_column')
    open_form('Form3')
    






  







