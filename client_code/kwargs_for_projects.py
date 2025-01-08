import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def search_projects_using_kwargs(self):
    
    kwargs ={}
    searchassigned = self.drop_down_1.selected_value
    
    print('search1', searchassigned)
    if searchassigned:
      kwargs['assigned_to'] = searchassigned
      
    dicts,Xmedia = anvil.server.call('get_orders', **kwargs )
    # search2 = self.multi_select_stage_dropdown.selected 
    # search3 = self.exclude_completed_checkbox.checked
    # search4 = self.project_count_sort_chkbox.checkeddef search_using_kwargs(self):
    # self.hits_textbox.text  = None
    # self.no_of_projects_textbox.text = None  
    
    # search1 = self.boards_dropdown.selected_value
    # search2 = self.multi_select_stage_dropdown.selected 
    # search3 = self.exclude_completed_checkbox.checked
    # search4 = self.project_count_sort_chkbox.checked