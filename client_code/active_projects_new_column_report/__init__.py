from ._anvil_designer import active_projects_new_column_reportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class active_projects_new_column_report(active_projects_new_column_reportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    boards =list({(r['project_board']) for r in app_tables.projects.search(tables.order_by('project_board'))})
    self.project_board_dropdown.items = boards
    # Any code you write here will run before the form opens.
    # dicts_boards =anvil.server.call('active_board_stages')
    # print(dicts_boards)

    # self.repeating_panel_1.items = dicts_boards




  def project_board_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    board = self.project_board_dropdown.selected_value
    print('selected board =', board)
    dicts_boards =anvil.server.call('active_board_stages',board)
    # forms = self.repeating_panel_1.get_components()
    # filter_list = self.project_board_dropdown.selected_value
    # for form in forms:
    # #check if brand is in filter list
    #       if form.item['project_board'] in filter_list:
    # #if brand is in list make item visable
    #         form.visible = True
    #       else:
    # #if brand not in list make item hidden
    #         form.visible = False
    # pass

