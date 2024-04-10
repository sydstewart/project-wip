from ._anvil_designer import changes_projectsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class changes_projects(changes_projectsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.elapsed_days_sort_checkbox.checked = False
    self.percent_complete_sort_checkbox.checked = False
    self.managers_dropdown.items = anvil.server.call('managers_list')
    # print('managers', managers)
    # managers = managers.sort()
    # print('managers', managers)
    dicts, count_found = anvil.server.call('show_changes')
    self.repeating_panel_1.items = dicts


  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('send_pdf_email')

  def populate_Burndown_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts = anvil.server.call('burndown')
    self.repeating_panel_1.items = dicts
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    dicts, projects = anvil.server.call('show_progress',self.project_drop_down.selected_value)

    self.project_drop_down.items = projects
    self.repeating_panel_1.items = dicts
    pass

  def managers_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.elapsed_days_sort_checkbox.checked = False
    self.percent_complete_sort_checkbox.checked = False
    self.days_since_updated_checkbox.checked = False
    user = self.managers_dropdown.selected_value
    user = user['email']
    print(user)
    dicts, fig, count_found = anvil.server.call('show_progress_managers', user)
    if count_found > 0 :
      self.repeating_panel_1.items =  sorted(dicts, key=lambda row: row['latest_percent_complete'])
      layout = {
          'title': 'Heat Map of Projects created at ' + datetime.now().strftime('%d %B %Y %H:%M') + ' for ' + user,
          'yaxis': {'title': 'Percentage complete', 'range' :[-5, 104]},
          'xaxis': {'x0': 0,'title': 'Days Elapsed'},

        }
      # line_plots = anvil.server.call('individual_chart',self.project_drop_down.selected_value)
      self.plot_1.figure = fig
      # self.plot_1.data = line_plots
      # # self.project_drop_down.items = projects
      self.repeating_panel_1.items = dicts
    else:
      alert('No Projects Found for ' + user)
    pass

  def percent_complete_sort_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    # user = self.managers_dropdown.selected_value
    # user = user['email']
    # dicts, line_plots = anvil.server.call('show_progress_managers', user)
    self.elapsed_days_sort_checkbox.checked = False
    self.days_since_updated_checkbox.checked = False
    if self.percent_complete_sort_checkbox.checked == True:
      # self.repeating_panel_1.items = dicts
      self.repeating_panel_1.items =  sorted(self.repeating_panel_1.items, key=lambda row: row['latest_percent_complete'], reverse = True)
    else:
      # self.repeating_panel_1.items = dicts
      self.repeating_panel_1.items =  sorted(self.repeating_panel_1.items, key=lambda row: row['latest_percent_complete'], reverse = False)
      pass

  def elapsed_days_sort_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.percent_complete_sort_checkbox.checked = False
    self.days_since_updated_checkbox.checked = False
    if self.elapsed_days_sort_checkbox.checked ==  True:
      self.repeating_panel_1.items =  sorted(self.repeating_panel_1.items, key=lambda row: row['elapsed_time'], reverse = True)
    else:
      self.repeating_panel_1.items =  sorted(self.repeating_panel_1.items, key=lambda row: row['elapsed_time'], reverse = False)

  def days_since_updated_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.percent_complete_sort_checkbox.checked = False
    self.elapsed_days_sort_checkbox.checked = False
    if self.days_since_updated_checkbox.checked == True:
      self.repeating_panel_1.items =  sorted(self.repeating_panel_1.items, key=lambda row: row['days_since_updated'], reverse = True)
    else:
      self.repeating_panel_1.items =  sorted(self.repeating_panel_1.items, key=lambda row: row['days_since_updated'], reverse = False)
    pass
