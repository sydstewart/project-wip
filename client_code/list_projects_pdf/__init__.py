from ._anvil_designer import list_projects_pdfTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media


class list_projects_pdf(list_projects_pdfTemplate):
  def __init__(self, dicts, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = dicts
    # print("Percent Complete=", self.percent_complete_text_box.text)
    # print("Assigned to =", self.drop_down_1.selected_value)
    # print("Catgeory =", self.Category.selected_value)
    # dicts, Xmedia = anvil.server.call(
    #   "generate_pdf",
    #  pdf_info
    # )
    # # self.text_box_1.text = len(dicts)
    # # self.repeating_panel_1.items = dicts

  def percent_complete_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    print("Percent Complete=", self.percent_complete_text_box.text)
    print("Assigned to =", self.drop_down_1.selected_value)
    print("Catgeory =", self.Category.selected_value)
    dicts, Xmedia = anvil.server.call(
      "get_orders",
      self.percent_complete_text_box.text,
      self.drop_down_1.selected_value,
      self.Category.selected_value,
    )
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    print("Percent Complete=", self.percent_complete_text_box.text)
    print("Assigned to =", self.drop_down_1.selected_value)
    print("Catgeory =", self.Category.selected_value)
    dicts, Xmedia = anvil.server.call(
      "get_orders",
      self.percent_complete_text_box.text,
      self.drop_down_1.selected_value,
      self.Category.selected_value,
    )
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    pass

  def Category_change(self, **event_args):
    """This method is called when an item is selected"""
    print("Percent Complete=", self.percent_complete_text_box.text)
    print("Assigned to =", self.drop_down_1.selected_value)
    print("Category =", self.Category.selected_value)
    dicts, Xmedia = anvil.server.call(
      "get_orders",
      self.percent_complete_text_box.text,
      self.drop_down_1.selected_value,
      self.Category.selected_value,
    )
    self.text_box_1.text = len(dicts)
    self.repeating_panel_1.items = dicts
    pass

  def download_PDF_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # start = self.level_textbox.text
    # pdf_info = {
    #   "percent_complete": self.percent_complete_text_box.text,
    #   "assigned to": self.drop_down_1.selected_valuet,
    #   "category": self.Category.selected_value,
    # }
    # media_object = anvil.server.call("generate_pdf", pdf_info)
    # # dicts, Xmedia = anvil.server.call('get_orders', self.percent_complete_text_box.text,self.drop_down_1.selected_value, self.Category.selected_value)
    # download(media_object)
    # # pdfdata =anvil.server.call('create_projects_pdf', dicts)
    # # download(pdfdata)
    # # # anvil.media.download(media_object)
    # pass
    # pass