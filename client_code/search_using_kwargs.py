import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def search_using_kwargs(self):
    kwargs ={}
 

    search1 = self.board_dropdown.selected
    search2 = self.New_stage_dropdown.selected_value
    if  search1:
        kwargs['project_board']=q.any_of(*search1)
    if search2:
        old_stages = app_tables.stage_translate.search(new_column = search2)
        thislist =[]
        for row in old_stages:
            thislist.append(row['project_column'])
          
        kwargs['project_column']=q.any_of(*thislist)
      
    results = app_tables.projects.search(**kwargs)

    self.repeating_panel_1.items = results
    # self.hits_textbox.text  = len(results)