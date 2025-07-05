from ._anvil_designer import TestSydTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil_extras import navigation
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Derived from the Anvil Extras Demo published at https://github.com/anvilistas/anvil-extras


@navigation.register(name="TestSyd", title="Test Syd")

class TestSyd(TestSydTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
