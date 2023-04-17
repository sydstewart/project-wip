import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module3
#
#    Module3.say_hello()
#
def background_check_tick(self, **event_args):
    task_status = anvil.server.call_s('get_status', id=self.task_id)
    if task_status:
      self.task_status_label.text = task_status
    else:
      self.task_status_label.text = 'Done!'
      self.background_check.interval = 0
