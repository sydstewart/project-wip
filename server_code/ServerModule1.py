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
  print(task.get_state())

  # Is the task complete yet?
  if task.is_completed():
    return task
  

@anvil.server.background_task
def listprojects():
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
  dicts =[]
  for r in cur.fetchall():
      if r['stage'] in ['10. Scheduled',	'Planned','Planning','Scheduled','To be re-visited','Today...','To Do']:
        x_column = '00. Planned'
        print(x_column)
        dicts = dicts.append[{'project_board': r['boards'],'project_column':r['stage'], 'count' : r['count'], 'new_stage': x_column}]  
      elif r['stage'] in ['05. Enquiry Not yet started', 	'05. Enquiry - Not Yet Started'	]:
        x_column = '01. Enquiry'
        print(x_column)
        dicts = dicts.append[{'project_board': r['boards'],'project_column':r['stage'], 'count' : r['count'], 'new_stage': x_column}]  
      elif r['stage'] in ['10. Order Approved',	'Ordered'	]:
        x_column = '02. Order Approved'
        print(x_column)
        dicts = dicts.append[{'project_board': r['boards'],'project_column':r['stage'], 'count' : r['count'], 'new_stage': x_column}]  
  for d in dicts:
                                  
            app_tables.projects_stages.add_row(**d)
#             getstagerow = app_tables.projects_stages.get(project_board= d['project_board'], project_column=d['project_column'])
  #=================================================================================
#   # Load Projects into separate table          
#   with conn.cursor() as cur1:
#       cur1.execute(
#          "Select  portfolioboards.boardName as boards, teamwork.portfoliocolumns.columnName as stage, teamwork.projects.projectname as project_name \
#           From teamwork.portfoliocards Join \
#               teamwork.projects On teamwork.portfoliocards.projectId = \
#               teamwork.projects.projectId Join \
#               teamwork.portfoliocolumns On teamwork.portfoliocards.columnId = \
#               teamwork.portfoliocolumns.columnId Join \
#               teamwork.portfolioboards On teamwork.portfolioboards.boardId = \
#               teamwork.portfoliocards.boardId \
#       Where projectStatus = 'active' And cardStatus = 'ACTIVE'"  
#     ) 
    
#   print('starting to load projects')
#   for r in cur1.fetchall(): 
#         dicts = [{'project_name' : r['project_name'],'project_board': r['boards'],'project_column':r['stage']}]
#         for d in dicts:
#               getstagerow = app_tables.projects_stages.get(project_board= d['project_board'], project_column=d['project_column'])
                                
#               app_tables.projects.add_row( **d)
    
# # Link Tables
#   print('Starting to Link')
#   for p in app_tables.projects.search():
#                 getstagerow = app_tables.projects_stages.get(project_board= p['project_board'], project_column=p['project_column'])
#                 p.update(project_stages = getstagerow)   
        
        
        
# # link to Project_column translate

#   for x in app_tables.projects.search():
#                 getsNewstagerow = app_tables.stage_translate.get(project_column=x['project_column'])
#                 x.update(new_stages = getsNewstagerow) 
#   for y in app_tables.projects_stages.search():
#                 getsNewstagerow = app_tables.stage_translate.get(project_column=y['project_column'])
#                 y.update(new_project_column = getsNewstagerow)     
    
        