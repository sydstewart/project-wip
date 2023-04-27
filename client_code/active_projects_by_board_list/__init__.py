from ._anvil_designer import active_projects_by_board_listTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class active_projects_by_board_list(active_projects_by_board_listTemplate):
  def __init__(self, project_board, **properties):

    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.project_board_textbox.text = project_board
    # self.project_column_textbox.text = project_column
    # Any code you write here will run before the form opens.
    # print('Project board of line', project_board, project_column)
    self.repeating_panel_1.items = app_tables.projects.search(project_column = q.not_('40. Done',	'90. Completed',	'90. Gone Live - Completed', \
                                                                            'Done',	'Lost/Closed','15. Free of Charge','90. Gone Live - Completed', \
                                                                            'Released','Archive','To Archive','Archived', '10. Order Approved','Ordered',  \
                                                                             '10. Scheduled','To Do', 'To be re-visited','Planning','Planned')  \
                                                                            , project_board = project_board)