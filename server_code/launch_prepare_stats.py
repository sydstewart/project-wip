import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server

@anvil.server.callable
def prepare_stats_launch():
  """Launch a single stats background task."""
  task = anvil.server.launch_background_task('prepare_stats')
  return task  