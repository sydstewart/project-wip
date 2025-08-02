from ._anvil_designer import projects_in_progress_new_copyTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.tz
from ..repeating_panel_calcs import repeating_panel_calcs
 

class projects_in_progress_new_copy(projects_in_progress_new_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    repeating_panel_calcs(self)
    # dicts,Xmedia  = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    # dicts, dictspip, dictswts, dictsoh, Xmedia,pivotsyd_to_markdown  = anvil.server.call('get_orders_for_pivots', 0, 100, None, None, None)
    # a1 = str(len(dictspip))
    # a = "Projects in Progress at"
    # b = (datetime.now().strftime("%Y-%m-%d"))
    # self.label_1.text = a1 + " " + a + " " + b

    # order_total = (sum(item['order_value']
    #                            for item in self.repeating_panel_1.items))
    # order_total= str('£' + str(round(order_total)))
    # self.label_5.text = order_total

    # days_elapsed_sum = (sum(item['days_elapsed']
    #                    for item in self.repeating_panel_1.items))
    # days_elapsed_average= (round(days_elapsed_sum))/len(self.repeating_panel_1.items)
    # days_elapsed_average= str(round(days_elapsed_average))
    # self.label_4.text = days_elapsed_average

    # work_to_do_sum = (sum(item['Work To Do']
    #                         for item in self.repeating_panel_1.items))
    # work_to_do_sum= str('£' + str(round(work_to_do_sum)))
    # self.label_8.text = work_to_do_sum

    # percent_complete_sum = (sum(item['percent_complete']
    #                         for item in self.repeating_panel_1.items))
    # percent_complete_average= (round(percent_complete_sum ))/len(self.repeating_panel_1.items)
    # percent_complete_average= str(round(percent_complete_average))
    # self.label_10.text = percent_complete_average

    # self.repeating_panel_1.items.append({'order_value_formated': order_total, 'days_elapsed': days_elapsed_average })
    # self.repeating_panel_1.items = self.repeating_panel_1.items
    # Any code you write here will run before the form opens.

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_2.checked = False
    self.check_box_3.checked = False
    self.check_box_4.checked = False
    self.check_box_5.checked = False
    self.repeating_panel_1.items = sorted(
      [r for r in self.repeating_panel_1.items],
      key=lambda x: (x["percent_complete"]),
      reverse=True,
    )

    pass

  def check_box_2_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_1.checked = False
    self.check_box_3.checked = False
    self.check_box_4.checked = False
    self.check_box_5.checked = False
    self.repeating_panel_1.items = sorted(
      [r for r in self.repeating_panel_1.items],
      key=lambda x: (x["Value yet to be invoiced"]),
      reverse=True,
    )

    pass

  def check_box_3_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_1.checked = False
    self.check_box_2.checked = False
    self.check_box_4.checked = False
    self.check_box_5.checked = False
    self.repeating_panel_1.items = sorted(
      [r for r in self.repeating_panel_1.items],
      key=lambda x: (x["days_elapsed"]),
      reverse=True,
    )

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""

    media_object = anvil.server.call("create_zaphod_pdf", projects_in_progress_new)
    anvil.media.download(media_object)

  def check_box_4_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_2.checked = False
    self.check_box_3.checked = False
    self.check_box_1.checked = False
    self.check_box_5.checked = False
    self.repeating_panel_1.items = sorted(
      [r for r in self.repeating_panel_1.items],
      key=lambda x: (x["Work To Do"]),
      reverse=True,
    )

    pass
    pass

  def check_box_5_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.check_box_2.checked = False
    self.check_box_3.checked = False
    self.check_box_1.checked = False
    self.check_box_4.checked = False
    self.repeating_panel_1.items = sorted(
      [r for r in self.repeating_panel_1.items],
      key=lambda x: (x["order_value"]),
      reverse=True,
    )
    pass

  def waiting_on_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    # repeating_panel_calcs(self)
    # self.repeating_panel_1.items = my_global
    self.repeating_panel_1.items = [item for item in self.repeating_panel_1.items if item['waiting_on'] == self.waiting_on_dropdown.selected_value]


    pass
