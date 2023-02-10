from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Module1  import show_projects
from ...Form2 import Form2
# from .. from 
class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_projects_panel.visible = False
#     self.repeating_projects_panel.items = app_tables.projects.search(project_stages= project_stages)
    # Any code you write here will run before the form opens.
#     self.repeating_projects_panel.items = anvil.server.call('get_projects_in_project_stages', self.item)
#   def show_project_button_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     project_copy = dict(list(self.item))
#     # Open an alert displaying the 'ArticleEdit' Form
#     # set the `self.item` property of the ArticleEdit Form to a copy of the article to be updated
# #     projects = app_tables.projects_stages.search(project_board = project_copy['project_board'], project_column=project_copy['project_column'])

    
#     content = project_list(project_board = project_copy['project_board'], project_column=project_copy['project_column'])
#     result = alert(content, buttons=[], title = 'Projects', large=True)
    
    
 
   

  def show_project_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print('Project board of line', self.item['project_board'])
    result = alert(content=Form2(self.item['project_board'], self.item['project_column']), title="Projects", buttons=[], large=True)
    
#     show_projects(self)
#     if self.repeating_projects_panel.visible == False:
#         self.repeating_projects_panel.visible = True
#     else:
#         self.repeating_projects_panel.visible = False
#     pass

  def text_box_2_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass




 