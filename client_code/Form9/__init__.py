from ._anvil_designer import Form9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.http
from anvil.tables import app_tables
from ..pie_charts_new import pie_charts_new
from ..pivots_new import pivots_new
from ..Run_Chart_New import Run_Chart_New
from ..stage_group_new_chart import stage_group_new_chart
from ..projects_in_progress_new import projects_in_progress_new
from ..projects_waiting_to_start_new import projects_waiting_to_start_new
from ..projects_on_hold_new import projects_on_hold_new
from ..Testquery import Testquery
from ..Form12 import Form12
from ..Form14 import Form14
from ..Form15 import Form15

def reset_links(self):
 
  self.link_1.role = None
  self.link_2.role = None
  self.link_3.role = None
  self.link_4.role = None
  self.link_5.role = None
  self.link_6.role = None
  self.link_7.role = None
  self.link_11.role = None
  self.link_12.role = None
  
  pass
  
class Form9(Form9Template):
  def __init__(self, **properties):
 
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.link_6_click()
    # self.add_component(Label(text= '     Project WIP'), slot='title')
    anvil.users.login_with_form()
    loggedin_user = anvil.users.get_user()
    username = loggedin_user['email']
    usertype = anvil.server.call('get_user_type',loggedin_user)
    print('User -',username)
    print('User -',usertype)
   
    # myip=anvil.http.request("https://6JUQ62P5MFEPKLVW.anvilapp.net/_/api/tools/myip")
     
    # print(myip)
     
 

    self.label_1.text = 'User is ' + username + ' ' + usertype
    
    # self.text_box_2.text = loggedin_user['user_type']
    # self.text_box_1.text = username 
    # organisation = loggedin_user['Organisation']
    # Globals.loggedin_user = loggedin_user
    # Globals.organisation = organisation
    if usertype != 'admin': 
        self.link_11.visible = False
        self.link_12.visible = False
        self.link_8.visible = False
        self.link_9.visible = False
        self.link_10.visible = False
        # self.link_10.visible = False
        
    

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    # self.reset_links()
    # self.link_1.role = 'selected'
    reset_links(self)
    self.link_1.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(pie_charts_new(), full_width_row=True)
    # self.link_3.role = ''
    # self.reset_links()
    pass

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_2.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(pivots_new(), full_width_row=True)
    # self.reset_links()
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_3.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(Run_Chart_New(), full_width_row=True)
    # self.reset_links()
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_4.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(stage_group_new_chart(), full_width_row=True)
    pass

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_5.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(Form14(), full_width_row=True)
    pass

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_6.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(Form12(), full_width_row=True)
    pass

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_7.role = 'selected'
    self.content_panel.clear()
    self.content_panel.add_component(Form15(), full_width_row=True)
    pass

    
    # self.content_panel.add_component(projects_on_hold_new(), full_width_row=True)
    pass
   
  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.task = anvil.server.call('prepare_stage_changes_launch')

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('prepare_percent_launch')
    pass

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.task = anvil.server.call('prepare_wait_changes_launch')
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.column_panel_1.clear()

    anvil.users.logout()

    anvil.users.login_with_form()
    open_form('Form9')
    pass

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_11.role = 'selected'
    self.task = anvil.server.call('daily_stats_trial')
    pass

  def link_12_click(self, **event_args):
    """This method is called when the link is clicked"""
    reset_links(self)
    self.link_12.role = 'selected'
    self.task = anvil.server.call('prepare_stats_launch')
    pass
    


