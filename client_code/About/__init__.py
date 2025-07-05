from ._anvil_designer import AboutTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import navigation

@navigation.register(name="About", title="About")
class About(AboutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.content_panel.visible
    self.label_1.text = 'Hello'
    # Any code you write here will run before the form opens.
