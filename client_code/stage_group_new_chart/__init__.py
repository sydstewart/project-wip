from ._anvil_designer import stage_group_new_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stage_group_new_chart(stage_group_new_chartTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        line_plots = anvil.server.call('stage_groups_chart')
        # # Make the multi-bar plot
        self.plot_1.figure = line_plots
        pass

    # Any code you write here will run before the form opens.
