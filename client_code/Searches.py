import anvil.server
# import anvil.users
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files 
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def search_using_kwargs(self):
      
    search1 = self.boards_dropdown.selected_value
#     search2 = self.text_search_box.text
#     search3 = self.interfaces_drop_down.selected_value
#     search4 = self.apparea_drop_down.selected_value
#     search5 = self.version_level_dropdown.selected_value 
#     search6 = self.NOT_interface_chkbox.checked
#     search7 = self.app_multi_select_drop_down.selected
#     search8 = self.region_dropdown.selected_value
#     search9 = self.customer_type_dropdown.selected_value
#     search10 = self.live_version_dropdown.selected 
#     search11 = self.database_version_dropdown.selected_value
#     search12 = self.operating_system_dropdown.selected_value
#     search13 = self.access_dropdown.selected_value
#     search14 = self.account_dropdown.selected

# # Handle Interacting Fields
#     if search4:
#        self.app_multi_select_drop_down.selected =None
#     if search7:
#        self.apparea_drop_down.selected_value = None
#     if search5:
#        self.live_version_dropdown.selected  = None 
#     if search10:
#        self.version_level_dropdown.selected_value = None
    
# Setup search dictionary
    kwargs ={}

   
#Boards
    if search1:
#         self.text_search_box.text = None
        kwargs['project_board'] = search1  #q.like('%'+ search1['InUseStatus'] + '%')
#     kwargs['InUseStatus'] ='Live'# 

# #Interfaces
#     if search3:
# #          self.text_search_box.text = None
#          selectedinterface = ('%' + search3['Interface_Type'] + '%')
#          kwargs['Interfaces'] = q.like('%'+ selectedinterface + '%') 
    
#     # NOT Interfaces
#     if search6 == True and search3:
#          selectedinterface = ('%' + search3['Interface_Type'] + '%')
#          kwargs['Interfaces'] = q.not_(q.like('%'+ selectedinterface + '%'))
    
# # Applications  
#     if  search7:
#         kwargs['CFApplicationArea']=q.any_of(*search7)
    
#     if search4:
#         selectedapparea = ('%' + search4['application_area'] + '%')
#         kwargs['CFApplicationArea'] = q.like(selectedapparea) 
    
# # Version Levels    
#     if search5 and not search10:
# #         self.text_search_box.text = None
#         kwargs['Version_Level'] = search5    
#     if search10 and not search5 :
#         kwargs['Live_version_no'] = q.any_of(*search10)

# # Regions
#     if search8:
# #       self.text_search_box.text = None
#       kwargs['Location_c'] = search8

# # Customer Type    
#     if search9:
#       kwargs['Customer_Type'] = search9
      
# #Database Version
#     if search11: # has blank entries
#      kwargs['Database_Version'] = search11
      
# #Operating Systems
#     if search12:
#         kwargs['Operating_System'] = search12
      
# #Remote_Access_Available
#     if search13:
#         kwargs['Remote_Access_Available'] = search13
    
#     print(kwargs)
#     results = app_tables.suppported_products.search(**kwargs)
# # Account
#     if search14:
#         kwargs['Account'] =  q.any_of(*search14)
    
    print(kwargs)
    results = app_tables.projects_stages.search(tables.order_by('project_column'),**kwargs, )

    self.repeating_panel_1.items = results
    self.hits_textbox.text  = len(results)