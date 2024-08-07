import anvil.email
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
import anvil.media
import pandas as pd
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta


@anvil.server.callable
def get_projects_in_project_stages(project):
   
  return app_tables.projects.search(project_stages=project)

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
def load_data():
  """Launch a single crawler background task."""
  task = anvil.server.launch_background_task('listprojects')
    # Output some state from the task
  print(task.get_state())
  if not task.is_completed():
    return task.get_state()
  # Is the task complete yet?
  if task.is_completed():
    return
  # anvil.server.task_state['progress'] = 'Progress'
  # # print(task.get_state())
  # # # Is the task complete yet?
  # # if task.is_completed():
  # #   anvil.server.task_state['completed'] = 'Completed'
  # #   self.task_status_label.text = anvil.server.task_state['completed'] 
  # #   return task
  

@anvil.server.background_task
def listprojects():
  # anvil.server.task_state['progress'] = 42.
  # print(task.get_state()['progress'])
  
  conn = connect()
#=============================================================================  
  # Load Project Stages summary
  with conn.cursor() as cur:
    cur.execute(
      "Select  portfolioboards.boardName as boards, teamwork.portfoliocolumns.columnName as stage, teamwork.projects.projectname ,count(*) as count\
       From teamwork.portfoliocards Join \
          teamwork.projects On teamwork.portfoliocards.projectId = \
          teamwork.projects.projectId Join \
          teamwork.portfoliocolumns On teamwork.portfoliocards.columnId = \
          teamwork.portfoliocolumns.columnId Join \
          teamwork.portfolioboards On teamwork.portfolioboards.boardId = \
          teamwork.portfoliocards.boardId \
      Where projectStatus = 'active' And cardStatus = 'ACTIVE' \
      group by  portfolioboards.boardName , portfoliocolumns.columnName \
      Order By teamwork.portfoliocolumns.columnName, cardDisplayOrder"
                    )   
    # "Select portfolioboards.boardName as boards, \
    # portfoliocolumns.columnName as stage, count(*) as count\
    # From projects Inner Join \
    # portfoliocards On projects.projectId = portfoliocards.projectId Inner Join \
    # portfolioboards On portfolioboards.boardId = portfoliocards.boardId Inner Join \
    # portfoliocolumns On portfoliocards.columnId = portfoliocolumns.columnId \
    # group by  portfolioboards.boardName , \
    # portfoliocolumns.columnName"

      
  
#==================================================================================
# Clear tables   
  app_tables.projects_stages.delete_all_rows()
  app_tables.projects.delete_all_rows()
#==========================================================================================    
  # load project_stages
  print('starting to load project_stages')
  for r in cur.fetchall():
#       new_column = app_tables.stage_translate.get(project_column=r['stage'])
#       x_column = new_column['new_column']
      dicts = [{'project_board': r['boards'],'project_column':r['stage'], 'count' : r['count']}] #, 'new_column': x_column
      for d in dicts:
                                  
            app_tables.projects_stages.add_row(**d)
#             getstagerow = app_tables.projects_stages.get(project_board= d['project_board'], project_column=d['project_column'])
  #=================================================================================
  # Load Projects into separate table          
  with conn.cursor() as cur1:
      cur1.execute(
         "Select  portfolioboards.boardName as boards, teamwork.portfoliocolumns.columnName as stage, teamwork.projects.projectname as project_name \
          From teamwork.portfoliocards Join \
              teamwork.projects On teamwork.portfoliocards.projectId = \
              teamwork.projects.projectId Join \
              teamwork.portfoliocolumns On teamwork.portfoliocards.columnId = \
              teamwork.portfoliocolumns.columnId Join \
              teamwork.portfolioboards On teamwork.portfolioboards.boardId = \
              teamwork.portfoliocards.boardId \
      Where projectStatus = 'active' And cardStatus = 'ACTIVE'"  
    ) 
    
  print('starting to load projects')
  for r in cur1.fetchall(): 
        dicts = [{'project_name' : r['project_name'],'project_board': r['boards'],'project_column':r['stage']}]
        for d in dicts:
              getstagerow = app_tables.projects_stages.get(project_board= d['project_board'], project_column=d['project_column'])
                                
              app_tables.projects.add_row( **d)
    
# Link Tables
  print('Starting to Link')
  for p in app_tables.projects.search():
                getstagerow = app_tables.projects_stages.get(project_board= p['project_board'], project_column=p['project_column'])
                p.update(project_stages = getstagerow)   
        
        
        
# link to Project_column translate

  for x in app_tables.projects.search():
                getsNewstagerow = app_tables.stage_translate.get(project_column=x['project_column'])
                x.update(new_stages = getsNewstagerow) 
  for y in app_tables.projects_stages.search():
                getsNewstagerow = app_tables.stage_translate.get(project_column=y['project_column'])
                y.update(new_project_column = getsNewstagerow)    


@anvil.server.callable
def get_status(id):
  task = anvil.server.get_background_task(id)
  if task.is_completed():
    return None
  else:
    return task.get_state()['progress']
 

def background_check_tick(self, **event_args):
    task_status = anvil.server.call_s('get_status', id=self.task_id)
    if task_status:
      self.task_status_label.text = task_status
    else:
      self.task_status_label.text = 'Done!'
      self.background_check.interval = 0

@anvil.server.callable
def store_data(file , tablename):
  with anvil.media.TempFile(file) as file_name:
    if file.content_type == 'text/csv':
      df = pd.read_csv(file_name)
    else:
      df = pd.read_excel(file_name)
    # df['Date_Entered'] = pd.to_datetime(df['Date_Entered'], format='%d/%m/%Y')
    for d in df.to_dict(orient="records"):
      # d is now a dict of {columnname -> value} for this row
      # We use Python's **kwargs syntax to pass the whole dict as
      # keyword arguments
      getattr(app_tables, tablename).add_row(**d)

@anvil.server.callable
def get_Daily_WIP():
   dataWIP = app_tables.daily_wip.search(tables.order_by("Date_of_WIP", ascending=False))
   return dataWIP