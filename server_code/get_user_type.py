# import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# import anvil.email
import anvil.server



@anvil.server.callable
def get_user_type(loggedinuser):

  t = app_tables.users.get(email = loggedinuser['email']) 
  user_type = t['user_type']
  return user_type

