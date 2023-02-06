import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pymysql
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

def connect():
  connection = pymysql.connect(host='51.141.236.29',
                               port=3306,
                               user='CRMReadOnly',
                               password=anvil.secrets.get_secret('Teamwork Pass'),
                               database = 'teamwork',
                               cursorclass=pymysql.cursors.DictCursor)
  if not connection:
     alert(' Connection down')
  return connection


@anvil.server.callable
def listprojects():
  conn = connect()
  with conn.cursor() as cur:
   cur.execute(
    "Select projects.projectname as projects, portfolioboards.boardName as boards, \
    portfoliocolumns.columnName as stage \
    From projects Inner Join \
    portfoliocards On projects.projectId = portfoliocards.projectId Inner Join \
    portfolioboards On portfolioboards.boardId = portfoliocards.boardId Inner Join \
    portfoliocolumns On portfoliocards.columnId = portfoliocolumns.columnId"
   ) 
   
  app_tables.projects_stages.delete_all_rows()
   
  for r in cur.fetchall(): 
      dicts = [{'project_name': r['projects'],'project_board': r['boards'],'project_column':r['stage']}]
      for d in dicts:
                                  
            app_tables.projects_stages.add_row(**d)
            
  