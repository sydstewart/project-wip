from ._anvil_designer import pivots_newTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from anvil_extras import navigation
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Derived from the Anvil Extras Demo published at https://github.com/anvilistas/anvil-extras


@navigation.register(name="pivots_new", title="Pivots")
class pivots_new(pivots_newTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dicts = anvil.server.call('get_orders_for_pivots')

    self.pivot_1.items = dicts
    # Any code you write here will run before the form opens.
