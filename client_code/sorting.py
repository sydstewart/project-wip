import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
def set_sorting(self, object_name, column_name, **event_args):
    """This method is called when the link is clicked, sort after ACN column"""
    sorting_way = None#variable for sorting order
    list_all_links = [self.link_1, self.link_3, self.link_8, self.link_4]
    #check if some other column were already sorted and set their icon back to the normal unsorted state
    for links in list_all_links:
      if object_name != links:
        links.icon = 'fa:sort'
    #change icon of sorted column
    if object_name.icon == 'fa:sort':#never sorted
      object_name.icon = 'fa:sort-asc'#set ascending
      sorting_way = False # ascending
    elif object_name.icon == 'fa:sort-asc':#already sorted as ascending
      object_name.icon = 'fa:sort-desc'#set descending
      sorting_way = True # descending
    elif object_name.icon == 'fa:sort-desc':#once again get back to ascending
      object_name.icon = 'fa:sort-asc'
      sorting_way = False # ascending
    sorting_function(self, column_name,sorting_way)
    pass

def sorting_function(self, column_name, sorting_way):
    """function used for sorting in combination with headers"""
    # self.lb_sort_col.text = column_name
    # if sorting_way == True:
    #   self.lb_asc_dsc.text = 'dsc'
    # else:
    #   self.lb_asc_dsc.text = 'asc'
    # if int(self.total.text) < 2000: #large data need to be sorted on server side by a new call
    key_func = lambda x: x[column_name]
    # if column_name == 'DUMMY':  # replace 'user_column' with the actual name of the column, replace DUMMY to make an exception for user columns
    # key_func = lambda x: x[column_name]['email']  # replace 'email' with the actual key for the user email
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items],
                                                key=key_func,
                                                reverse=sorting_way)
