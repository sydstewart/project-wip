import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def search_using_kwargs(self):
    kwargs ={}
 

    search1 = self.board_dropdown.selected
    # search2 = self.New_stage_dropdown.selected_value
    # search3 = self.exclude_archived_completed.checked
    if  search1:
        kwargs[0]=X['assigned_to']= search1
    print('kwargs', kwargs)
    # if search2:
    #     old_stages = app_tables.stage_translate.search(new_column = search2)
    #     thislist =[]
    #     for row in old_stages:
    #         thislist.append(row['project_column'])
          
    #     kwargs['project_column']=q.any_of(*thislist)
    #       # Not  completed
    # if search3 == True and search2:   
    #      kwargs['project_column'] =q.all_of(q.not_('40. Done',	'90. Completed',	'90. Gone Live - Completed', \
    #                                                                         'Done',	'Lost/Closed','15. Free of Charge','90. Gone Live - Completed', \
    #                                                                         'Released','Archive','To Archive','Archived'))
    #      kwargs['project_column']=q.any_of(*thislist)
    # if search3 == True and not  search2:
    #      kwargs['project_column'] = q.not_('90. Gone Live - Completed','40. Done','Released','Archive','Done','To Archive','Archived')
      
      
    results = app_tables.projects.search(**kwargs)

    self.repeating_panel_1.items = results
    self.no_of_projects_found.text = len(self.repeating_panel_1.items )
    # self.hits_textbox.text  = len(results)