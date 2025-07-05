from ._anvil_designer import New_Home_MenuTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import navigation
from .. import pie_chart
from .. import About
from .. import Run_Chart

menu = [
  dict(text="Pie Charts", target="pie_chart", icon="fa:wrench", bold=True),
  dict(text="Run Charts", target="Run_Chart", icon="fa:link"), 
  dict(text="About", target="About", icon="fa:comments-o"),
  # dict(text="PageBreak", target="page_break", icon="fa:file-pdf-o"),
  # dict(text="Local Storage", target="storage", icon="fa:floppy-o"),
]
# menu_items = [
#   # {"text": "Home", "target": "pie_chart"},
#   {"text": "Pie Charts", "target": "pie_chart"},
#   {"text": "Run Charts", "target": "Run_Chart"},
#   {"text": "About", "target": "About"}
# ]
# @navigation.register(name="pie_chart", title="Home Menu")
# @navigation.register("New_Home_Menu")
# @routing.main_router
class New_Home_Menu(New_Home_MenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    navigation.build_menu(self.menu_panel, menu)
    self.init_components(**properties)
    # navigation.go_to("Run_Chart")
    # Any code you write here will run before the form opens.
  def form_show(self, **event_args):
      """This method is called when the HTML panel is shown on the screen"""
      navigation.go_to("Run_Chart")
  