import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
import numpy as np
from datetime import datetime, time , date , timedelta

@anvil.server.background_task
@anvil.tables.in_transaction
def prepare_stats():
      # dicts,dictspip, dictswts, dictsoh, X_media,  pivotsyd_to_markdown= prepare_pandas(dicts, 0, None, None, None, None)
      # app_tables.stage_summary.delete_all_rows()
      dicts = app_tables.sales_orders_all.search()
      X = pd.DataFrame.from_dict(dicts)
      #======================Overall Totals======================================
      wiplist = ['Work in Progress', 'On Hold','Waiting to Start']
      filtered_df = X[X['stage_group'].isin(wiplist )  ]
      total_order_value = filtered_df['order_value'].sum()
      # print( 'Total value Order', total_order_value )
      overall_percentage_completion =  filtered_df['percent_complete'].mean()
      print( 'Overall Percent Complete', overall_percentage_completion )
      total_partially_invoiced = filtered_df['partially_invoiced_total'].sum()
      print( 'Total Partially Invoiced', total_partially_invoiced )
      total_project_count = filtered_df['order_value'].count()
      print( 'Total Project_Count', total_project_count )
      print('Waiting On',X['waiting_on'])
      print("========================================================")
      #=======================Projects on Hold ======================================
      
      filtered_df_on_hold = X[X['stage_group'] == 'On Hold'] 
      sum_of_onhold = filtered_df_on_hold['order_value'].sum()
      count_of_onhold = filtered_df_on_hold['order_value'].count()
      on_hold_percentage_complete_on_hold  = filtered_df_on_hold['percent_complete'].mean()
      work_completed_on_hold = sum_of_onhold * on_hold_percentage_complete_on_hold/100
      work_to_do_on_hold = sum_of_onhold - work_completed_on_hold 
      on_hold_total_partially_invoiced = filtered_df_on_hold['partially_invoiced_total'].sum()
      
      
      print('Total Projects on Hold', sum_of_onhold )
      print('on_hold_percentage_complete', on_hold_percentage_complete_on_hold)
      print('on_hold_work_to_do', work_to_do_on_hold )
      print('on hold Total  Partialy Invoiced', on_hold_total_partially_invoiced )
      print("========================================================")
      #=======================Projects Waiting to Start ======================================
      filtered_df_wait_to_start = X[X['stage_group'] == 'Waiting to Start'] 
      sum_of_onhold = filtered_df_wait_to_start ['order_value'].sum()
      print('Total Projects Waiting to Start', sum_of_onhold )
      
      
      print('#========================Projects in Progress======================================')
      
      filtered_df_wip = X[X['stage_group'] == 'Work in Progress'] 
      sum_of_in_progress = filtered_df_wip['order_value'].sum() 
      count_of_in_progress = filtered_df_wip['order_value'].count() 
      percentage_complete_in_progress  = filtered_df_wip['percent_complete'].mean()
      work_completed_in_progress= sum_of_in_progress * (percentage_complete_in_progress/100)
      work_to_do_in_progress = sum_of_in_progress  - work_completed_in_progress
      in_progress_total_partially_invoiced = filtered_df_wip['partially_invoiced_total'].sum()
      
      #====wait of Customer in Work in Progress
      filtered_df_wait = filtered_df_wip[filtered_df_wip['waiting_on'] == 'Customer']
      if filtered_df_wait.empty is False:
          sum_of_waiting_in_progress_waiting_on_customer = filtered_df_wait['order_value'].sum()
          count_of_waiting_in_progress_waiting_on_customer = filtered_df_wait['order_no'].count()
          percentage_complete_in_progress_waiting_on_customer   = filtered_df_wait['percent_complete'].mean()
          work_completed_in_progress_waiting_on_customer = sum_of_waiting_in_progress_waiting_on_customer * (percentage_complete_in_progress_waiting_on_customer/100)
          work_to_do_in_progress_in_progress_waiting_on_customer = sum_of_waiting_in_progress_waiting_on_customer  - work_completed_in_progress_waiting_on_customer
          print('Customer Waiting State', filtered_df_wait[['order_no','project_name','stage','order_value', 'percent_complete','waiting_on']])
      else:
        sum_of_waiting_in_progress_waiting_on_customer = 0
        count_of_waiting_in_progress_waiting_on_customer = 0
        percentage_complete_in_progress_waiting_on_customer   = 0
        work_completed_in_progress_waiting_on_customer = 0
        work_to_do_in_progress_in_progress_waiting_on_customer = 0
      #======Wait on 4S
      filtered_df_wait_4S = filtered_df_wip[filtered_df['waiting_on'] == '4S']
      if filtered_df_wait_4S.empty is False:
          sum_of_waiting_in_progress_waiting_on_4S = filtered_df_wait_4S['order_value'].sum()  
          count_of_waiting_in_progress_waiting_on_4S = filtered_df_wait_4S['order_no'].count() 
          percentage_complete_in_progress_waiting_on_4S  = filtered_df_wait_4S['percent_complete'].mean()
          work_completed_in_progress_waiting_on_4S= sum_of_waiting_in_progress_waiting_on_4S  * (percentage_complete_in_progress_waiting_on_4S/100)
          work_to_do_in_progress_in_progress_waiting_on_4S = sum_of_waiting_in_progress_waiting_on_4S  - work_completed_in_progress_waiting_on_4S
          print('4S Waiting State', filtered_df_wait_4S[['order_no','project_name','stage','order_value', 'percent_complete','waiting_on']])
      else:
        sum_of_waiting_in_progress_waiting_on_4S = 0
        count_of_waiting_in_progress_waiting_on_4S = 0
        percentage_complete_in_progress_waiting_on_4S  = 0
        work_completed_in_progress_waiting_on_4S= 0
        work_to_do_in_progress_in_progress_waiting_on_4S = 0
        
      #======Wait on no status
      filtered_df_wait_none = filtered_df_wip[filtered_df['waiting_on'] =='None']
      print('filtered_df_wait_none',filtered_df_wait_none)
      if filtered_df_wait_none.empty is False:
          sum_of_waiting_in_progress_waiting_no_state = filtered_df_wait_none['order_value'].sum()
          count_of_waiting_in_progress_waiting_no_state = filtered_df_wait_none['order_no'].count()
          percentage_complete_in_progress_waiting_no_state  = filtered_df_wait_none['percent_complete'].mean() 
          work_completed_in_progress_waiting_no_state= sum_of_waiting_in_progress_waiting_no_state  * (percentage_complete_in_progress_waiting_no_state/100)
          work_to_do_in_progress_in_progress_waiting_no_state = sum_of_waiting_in_progress_waiting_no_state  - work_completed_in_progress_waiting_no_state
          print('None Waiting State', filtered_df_wait_none[['order_no','project_name','stage','order_value', 'percent_complete','waiting_on']])
      else:
        sum_of_waiting_in_progress_waiting_no_state = 0
        count_of_waiting_in_progress_waiting_no_state = 0
        percentage_complete_in_progress_waiting_no_state  = 0
        work_completed_in_progress_waiting_no_state= 0
        work_to_do_in_progress_in_progress_waiting_no_state = 0
       
      
      print('================== Projects in progress Totals===================')
      print( 'Total Projects in Progress', sum_of_in_progress  )
      print('Total waiting on Customer',sum_of_waiting_in_progress_waiting_on_customer  )
      print('Total waiting on 4S',sum_of_waiting_in_progress_waiting_on_4S  ) 
      print('Total waiting no status ',sum_of_waiting_in_progress_waiting_no_state  ) 
      print('=============================================================') 
      
      print('================== Projects in progress Counts===================')
      print( 'Total count of Projects in Progress', count_of_in_progress   )
      print('Total count waiting on Customer',count_of_waiting_in_progress_waiting_on_customer  )
      print('Total count waiting on 4S',count_of_waiting_in_progress_waiting_on_4S ) 
      print('Total count waiting no status ',count_of_waiting_in_progress_waiting_no_state  ) 
      print('=============================================================') 
      
      print('================== Projects in progress percent complete===================')
      print( 'Average percent complete of Projects in Progress', percentage_complete_in_progress   )
      print('Average percent complete waiting on Customer',percentage_complete_in_progress_waiting_on_customer  )
      print('Average percent complete waiting on 4S',percentage_complete_in_progress_waiting_on_4S ) 
      print('Average percent complete waiting no status ',percentage_complete_in_progress_waiting_no_state  ) 
      print('=============================================================') 
      
      print('================== Projects in progress work Completed===================')
      print( 'Work complete of Projects in Progress', work_completed_in_progress   )
      print('Work complete waiting on Customer',work_completed_in_progress_waiting_on_customer  )
      print('Work Complete complete waiting on 4S',work_completed_in_progress_waiting_on_4S ) 
      print('Work complete waiting no status ', work_completed_in_progress_waiting_no_state ) 
      print('=============================================================') 
      
      print('================== Projects in progress work To Do===================')
      print( 'Work to do of Projects in Progress', work_to_do_in_progress )
      print('Work to do waiting on Customer',work_to_do_in_progress_in_progress_waiting_on_customer   )
      print('Work to do complete waiting on 4S',work_to_do_in_progress_in_progress_waiting_on_4S ) 
      print('Work to do waiting no status ', work_to_do_in_progress_in_progress_waiting_no_state ) 
      
      print('=============================================================')
      
      
      
      #=============================================================================
      #===============================================================================
      print('None Waiting State', filtered_df_wait_none[['order_no','project_name','stage','order_value', 'percent_complete']])
      print('in_progress_percentage_complete', percentage_complete_in_progress)
      print('in_progress_work_to_do', work_to_do_in_progress )
      print('in progress Total  Partialy Invoiced', in_progress_total_partially_invoiced  )
      
      print("========================================================")
      
      #=======================In Progress Waiting On Customer ================================
      filtered_df_wait = filtered_df_wip[filtered_df['waiting_on'] == 'Customer']
      sum_of_waiting_in_progress_waiting_on_customer = filtered_df_wait['order_value'].sum() 
      count_of_waiting_in_progress_waiting_on_customer = filtered_df_wait['order_value'].count() 
      percentage_complete_in_progress_waiting_on_customer   = filtered_df_wait['percent_complete'].mean()
      work_completed_in_progress_waiting_on_customer = sum_of_waiting_in_progress_waiting_on_customer * (percentage_complete_in_progress_waiting_on_customer/100)
      work_to_do_in_progress_in_progress_waiting_on_customer = sum_of_waiting_in_progress_waiting_on_customer  - work_completed_in_progress_waiting_on_customer
      print('Waiting Status',filtered_df_wait['waiting_on'])  
      count_of_waiting_in_progress_waiting_on_customer = filtered_df_wait['order_no'].count()
      sum_of_waiting_in_progress_waiting_on_customer = filtered_df_wait['order_value'].sum()
      print('============Waiting on Customer=====================')
      print('Total Order  Value of Projects In Progress waiting on customer', sum_of_waiting_in_progress_waiting_on_customer )
      print('Percent Completion of waiting on Customer', percentage_complete_in_progress_waiting_on_customer  )
      print('Total Work completed Value of Projects In Progress waiting on customer', work_completed_in_progress_waiting_on_customer  )
      print('Total Work to do Value of Projects In Progress waiting on customer', work_to_do_in_progress_in_progress_waiting_on_customer  )
      print("======================================")
      print('Count of Projects In Progress waiting on customer', count_of_waiting_in_progress_waiting_on_customer)
      print("======================================")
      #=======================In Progress Waiting None ================================
      filtered_df_wait = filtered_df_wip[filtered_df['waiting_on'].isnull()]
      print('Waiting Status',filtered_df_wait['waiting_on'])  
      # count_of_waiting_in_progress_waiting_no_state = filtered_df_wait['order_no'].count()
      # sum_of_waiting_in_progress_waiting_no_state = filtered_df_wait['order_value'].sum()
      # print('Total Order  Value of Projects In Progress waiting No State', sum_of_waiting_in_progress_waiting_no_state)
      # print('Count of Projects In Progress waiting No State', count_of_waiting_in_progress_waiting_no_state)
      print("======================================")
      #============================In Progress Waiting on 4S =====================================
      
      filtered_df_wait = filtered_df_wip[filtered_df['waiting_on'].str.contains("4S")]
      sum_of_waiting_in_progress_waiting_on_4S = filtered_df_wait['order_value'].sum() 
      count_of_waiting_in_progress_waiting_on_4S = filtered_df_wait['order_no'].count() 
      percentage_complete_in_progress_waiting_on_4S  = filtered_df_wait['percent_complete'].mean()
      work_completed_in_progress_waiting_on_4S= (sum_of_waiting_in_progress_waiting_on_4S  * percentage_complete_in_progress_waiting_on_4S)/100
      work_to_do_in_progress_in_progress_waiting_on_4S = sum_of_waiting_in_progress_waiting_on_4S  - work_completed_in_progress_waiting_on_4S
      # print('Waiting Status',filtered_df_wait['waiting_on'])  
      # count_of_waiting_in_progress_waiting_on_4S = filtered_df_wait['order_no'].count()
      # sum_of_waiting_in_progress_waiting_on_4S = filtered_df_wait['order_value'].sum()
      print('Count of Projects In Progresss waiting on 4S', count_of_waiting_in_progress_waiting_on_4S )
      print('Total Order  Value of Projects In Progress waiting on 4S', sum_of_waiting_in_progress_waiting_on_4S )
      print('Total Work Completed Value of Projects In Progress waiting on 4S', work_completed_in_progress_waiting_on_4S )
      print('Total Work to do Value of Projects In Progress waiting on 4S', work_to_do_in_progress_in_progress_waiting_on_4S  )
      print("========================================================")
      
      #=============================Projects Waiting to Start=================================
      
      filtered_df = X[X['stage_group'] == 'Waiting to Start'] 
      sum_of_waiting_to_start = filtered_df['order_value'].sum() 
      count_of_waiting_to_start = filtered_df['order_value'].count() 
      percentage_complete_to_start  = filtered_df['percent_complete'].mean()
      work_completed_to_start= sum_of_waiting_to_start* percentage_complete_to_start/100
      work_to_do_to_start = sum_of_waiting_to_start  - work_completed_to_start
      to_start_total_partially_invoiced = filtered_df['partially_invoiced_total'].sum()
      print('Total Projects Waiting to Start', sum_of_waiting_to_start) 
      print('iwaiting_to_start_percentage_complete', percentage_complete_to_start )
      print('to_start_work_to_do',  work_to_do_to_start )
      print('to start in progress Total  Partialy Invoiced', to_start_total_partially_invoiced)
      # print('X',X)
      print("========================================================")
      
      #====================================================================
      total_value_of_projects = sum_of_waiting_to_start + sum_of_in_progress  + sum_of_onhold
      total_work_to_do = work_to_do_to_start + work_to_do_in_progress + work_to_do_on_hold
      print('total_value_of_projects adding three Stage Groups',total_value_of_projects )
      print('total_value_of_projects work to do',total_work_to_do )
      today = datetime.today()


      app_tables.stage_summary.add_row(Date_of_WIP = (today),  Sum_on_hold = round(float(sum_of_onhold),0), 
                                      Sum_in_Progress = round(float(sum_of_in_progress ),0),
                                      Sum_in_Waiting_to_Start = round(float(sum_of_waiting_to_start),0),
                                      Total_Value_of_Projects = round(float(total_order_value),0),
      
                                      In_Progress_Waiting_on_Customer_count = round(float(count_of_waiting_in_progress_waiting_on_customer),0),
                                      In_Progress_Waiting_on_Customer_sum = round(float(sum_of_waiting_in_progress_waiting_on_customer),0),
                                      In_Progress_Waiting_on_Customer_sum_work_to_do = round(float(work_to_do_in_progress_in_progress_waiting_on_customer ),0),
                                      In_Progress_Waiting_on_Customer_percent_complete = round(float(percentage_complete_in_progress_waiting_on_customer),2),
                                      In_Progress_Waiting_on_Customer_work_complete = round(float(work_completed_in_progress_waiting_on_customer),1),
      
                                      In_Progress_Waiting_on_4S_count = round(float(count_of_waiting_in_progress_waiting_on_4S),0),
                                      In_Progress_Waiting_on_4S_sum = round(float(sum_of_waiting_in_progress_waiting_on_4S),0),
                                      In_Progress_Waiting_on_4S_sum_work_to_do = round(float(work_to_do_in_progress_in_progress_waiting_on_4S ),0),
                                      In_Progress_Waiting_on_4S_percent_complete = round(float(percentage_complete_in_progress_waiting_on_4S),2),
                                      In_Progress_Waiting_on_4S_work_complete = round(float(work_completed_in_progress_waiting_on_4S),1), 
      
                                      In_Progress_Waiting_no_state_count = round(float(count_of_waiting_in_progress_waiting_no_state),0),
                                      In_Progress_Waiting_no_state_sum   = round(float(sum_of_waiting_in_progress_waiting_no_state),0),
                                      In_Progress_Waiting_no_state_sum_work_to_do = round(float(work_to_do_in_progress_in_progress_waiting_no_state),0),
                                      In_Progress_Waiting_on_state_percent_complete = round(float( percentage_complete_in_progress_waiting_no_state),2),
                                      In_Progress_Waiting_no_state_work_complete  = round(float(work_completed_in_progress_waiting_no_state),1), 
      
                                      Percent_Completion_On_Hold = round(float(on_hold_percentage_complete_on_hold),1),
                                      Percent_Completion_in_Progress = round(float(percentage_complete_in_progress),1),
                                      Percent_Completion_to_start = round(float(percentage_complete_to_start),1),
                                      Overall_Percent_Completion =  round(float(overall_percentage_completion),1),
      
                                      Work_to_do_on_hold  = round(float(work_to_do_on_hold),0),
                                      Work_to_do_in_Progress= round(float(work_to_do_in_progress),0),
                                      Work_to_do_to_Start = round(float(work_to_do_to_start),0), 
                                      Total_Work_To_Do =  round(float(total_work_to_do),0),
      
                                      On_hold_Partially_Invoiced =  round(float(on_hold_total_partially_invoiced),0),
                                      To_Start_Partially_Invoiced = round(float(to_start_total_partially_invoiced),0), 
                                      In_Progress_Partially_Invoiced =  round(float(in_progress_total_partially_invoiced ),0),
                                      Total_Partially_Invoiced = round(float(total_partially_invoiced),0),
      
                                      Count_on_hold = count_of_onhold, 
                                      Count_in_Progress = count_of_in_progress,
                                      Count_of_waiting_to_start= count_of_waiting_to_start,
                                      Total_Project_Count = total_project_count)