from ._anvil_designer import Menu_NewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import navigation
from .. import pie_charts_new
from .. import About
from .. import Run_Chart_New
from .. import TestSyd
from .. import Sydney
from .. import Sheena
from .. import pivots_new
# navigation.set_mode("classic")
menu = [
  dict(text="Pie Charts", target="pie_charts_new", icon="fa:wrench"),
  dict(text="Run Chart", target="Run_Chart_New", icon="fa:link"), 
  dict(text="Pivots", target="pivots_new", icon="fa:comments-o"),
  # dict(text="Sheena", target="Sheena", icon="fa:comments-o"),
  # # dict(text="PageBreak", target="page_break", icon="fa:file-pdf-o"),
  # # dict(text="Local Storage", target="storage", icon="fa:floppy-o"),
]

class Menu_New(Menu_NewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    navigation.build_menu(self.menu_panel, menu)
    self.init_components(**properties)

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    navigation.go_to('pie_charts_new')
