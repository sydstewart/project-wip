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


def connect():
  connection = pymysql.connect(host='51.141.236.29',
                               port=3306,
                               user='CRMReadOnly',
                               password=anvil.secrets.get_secret('Teamwork Pass'),
                               database = 'infoathand',
                               cursorclass=pymysql.cursors.DictCursor)
  if not connection:
     alert(' Connection down')
  return connection
  
@anvil.server.callable
def wipprojects():
  
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur:
    cur.execute(
    "SELECT `sales_orders_cstm`.`AgreedLiveDate` AS `AgreedLiveDate`,\
    `sales_orders_cstm`.`EstimatedHoursWorkInvolved` AS `EstimatedHoursWorkInvolved`,\
    `sales_orders_cstm`.`GoLiveDate` AS `GoLiveDate`,\
    `sales_orders_cstm`.`Install_Config_Work_StartDate_Approx` AS `Install_Config_Work_StartDate_Approx`,\
    `sales_orders_cstm`.`Link` AS `Link`,\
    `sales_orders_cstm`.`OrderCategory` AS `OrderCategory`,\
    `sales_orders_cstm`.`StrategicallyImportant` AS `StrategicallyImportant`,\
    `sales_orders_cstm`.`ValueAdded` AS `ValueAdded`,\
    `accounts`.`account_number` AS `account_number`,\
    SUBSTRING(`accounts`.`account_popup`, 1, 1024) AS `account_popup`,\
    `accounts`.`account_popups` AS `account_popups`,\
    `accounts`.`account_type` AS `accounts_account_type`,\
    `accounts`.`annual_revenue` AS `accounts_annual_revenue`,\
    `accounts`.`assigned_user_id` AS `accounts_assigned_user_id_1`,\
    `accounts`.`balance` AS `accounts_balance`,\
    `accounts`.`balance_payable` AS `accounts_balance_payable`,\
    `accounts`.`billing_address_city` AS `accounts_billing_address_city_1`,\
    `accounts`.`billing_address_country` AS `accounts_billing_address_country_1`,\
    `accounts`.`billing_address_postalcode` AS `accounts_billing_address_postalcode_1`,\
    `accounts`.`billing_address_state` AS `accounts_billing_address_state_1`,\
    `accounts`.`billing_address_street` AS `accounts_billing_address_street_1`,\
    `accounts`.`created_by` AS `accounts_created_by_1`,\
    `accounts`.`credit_limit` AS `accounts_credit_limit`,\
    `accounts`.`credit_limit_usd` AS `accounts_credit_limit_usd`,\
    `accounts`.`currency_id` AS `accounts_currency_id_1`,\
    `accounts`.`date_entered` AS `accounts_date_entered_1`,\
    `accounts`.`date_modified` AS `accounts_date_modified_1`,\
    `accounts`.`default_discount_id` AS `accounts_default_discount_id`,\
    `accounts`.`default_purchase_discount_id` AS `accounts_default_purchase_discount_id`,\
    `accounts`.`default_purchase_shipper_id` AS `accounts_default_purchase_shipper_id`,\
    `accounts`.`default_purchase_terms` AS `accounts_default_purchase_terms`,\
    `accounts`.`default_shipper_id` AS `accounts_default_shipper_id`,\
    `accounts`.`default_terms` AS `accounts_default_terms`,\
    `accounts`.`deleted` AS `accounts_deleted_1`,\
    SUBSTRING(`accounts`.`description`,1,1024) AS `accounts_description_1`,\
    `accounts`.`email1` AS `accounts_email1`,\
    `accounts`.`email2` AS `accounts_email2`,\
    `accounts`.`email_opt_out` AS `accounts_email_opt_out`,\
    `accounts`.`employees` AS `accounts_employees`,\
    `accounts`.`exchange_rate` AS `accounts_exchange_rate_1`,\
    `accounts`.`first_invoice_id` AS `accounts_first_invoice_id`,\
    `accounts`.`id` AS `accounts_id_1`,\
    `accounts`.`industry` AS `accounts_industry`,\
    `accounts`.`invalid_email` AS `accounts_invalid_email`,\
    `accounts`.`is_supplier` AS `accounts_is_supplier`,\
    `accounts`.`last_invoice_id` AS `accounts_last_invoice_id`,\
    `accounts`.`main_service_contract_id` AS `accounts_main_service_contract_id`,\
    `accounts`.`modified_user_id` AS `accounts_modified_user_id_1`,\
    `accounts`.`name` AS `accounts_name_1`,\
    `accounts`.`ownership` AS `accounts_ownership`,\
    `accounts`.`parent_id` AS `accounts_parent_id`,\
    `accounts`.`partner` AS `accounts_partner`,\
    `accounts`.`partner_id` AS `accounts_partner_id`,\
    `accounts`.`phone_alternate` AS `accounts_phone_alternate`,\
    `accounts`.`phone_fax` AS `accounts_phone_fax`,\
    `accounts`.`phone_office` AS `accounts_phone_office`,\
    `accounts`.`primary_contact_id` AS `accounts_primary_contact_id`,\
    `accounts`.`purchase_credit_limit` AS `accounts_purchase_credit_limit`,\
    `accounts`.`purchase_credit_limit_usd` AS `accounts_purchase_credit_limit_usd`,\
    `accounts`.`rating` AS `accounts_rating`,\
    `accounts`.`shipping_address_city` AS `accounts_shipping_address_city_1`,\
    `accounts`.`shipping_address_country` AS `accounts_shipping_address_country_1`,\
    `accounts`.`shipping_address_postalcode` AS `accounts_shipping_address_postalcode_1`,\
    `accounts`.`shipping_address_state` AS `accounts_shipping_address_state_1`,\
    `accounts`.`shipping_address_street` AS `accounts_shipping_address_street_1`,\
    `accounts`.`sic_code` AS `accounts_sic_code`,\
    `accounts`.`tax_information` AS `accounts_tax_information_1`,\
    `accounts`.`temperature` AS `accounts_temperature`,\
    `accounts`.`ticker_symbol` AS `accounts_ticker_symbol`,\
    `accounts`.`website` AS `accounts_website`,\
    `sales_orders_cstm`.`acknowledgeorder_c` AS `acknowledgeorder_c`,\
    `users`.`address_city` AS `address_city`,\
    `users`.`address_country` AS `address_country`,\
    `users`.`address_format` AS `address_format`,\
    `users`.`address_postalcode` AS `address_postalcode`,\
    `users`.`address_state` AS `address_state`,\
    `users`.`address_street` AS `address_street`,\
    `sales_orders_cstm`.`addtoacbenchmarkscheme_c` AS `addtoacbenchmarkscheme_c`,\
    `sales_orders`.`amount` AS `amount`,\
    `sales_orders`.`amount_usdollar` AS `amount_usdollar`,\
    `sales_orders_cstm`.`applicationarea_c` AS `applicationarea_c`,\
    SUBSTRING(`sales_orders_cstm`.`approvalissues_c`, 1,1024) AS `approvalissues_c`,\
    `sales_orders`.`assigned_user_id` AS `assigned_user_id`,\
    `users`.`authenticate_id` AS `authenticate_id`,\
    `sales_orders`.`billing_account_id` AS `billing_account_id`,\
    `sales_orders`.`billing_address_city` AS `billing_address_city`,\
    `sales_orders`.`billing_address_country` AS `billing_address_country`,\
    `accounts`.`billing_address_countrycode` AS `billing_address_countrycode (accounts)`,\
    `sales_orders`.`billing_address_countrycode` AS `billing_address_countrycode`,\
    `sales_orders`.`billing_address_postalcode` AS `billing_address_postalcode`,\
    `sales_orders`.`billing_address_state` AS `billing_address_state`,\
    `accounts`.`billing_address_statecode` AS `billing_address_statecode (accounts)`,\
    `sales_orders`.`billing_address_statecode` AS `billing_address_statecode`,\
    `sales_orders`.`billing_address_street` AS `billing_address_street`,\
    `sales_orders`.`billing_contact_id` AS `billing_contact_id`,\
    `sales_orders`.`created_by` AS `created_by`,\
    `sales_orders`.`currency_id` AS `currency_id`,\
    `accounts`.`customer_level_id` AS `customer_level_id`,\
    `sales_orders_cstm`.`customer_responsiveness_c` AS `customer_responsiveness_c`,\
    `sales_orders`.`date_entered` AS `date_entered`,\
    `sales_orders`.`date_modified` AS `date_modified`,\
    `sales_orders_cstm`.`dateorderreceived_c` AS `dateorderreceived_c`,\
    `users`.`day_begin_hour` AS `day_begin_hour`,\
    `users`.`day_end_hour` AS `day_end_hour`,\
    `accounts`.`default_pricebook_id` AS `default_pricebook_id`,\
    `sales_orders`.`deleted` AS `deleted`,\
    `sales_orders`.`delivery_date` AS `delivery_date`,\
    `users`.`department` AS `department`,\
    SUBSTRING(`sales_orders`.`description`,1, 1024) AS `description`,\
    `sales_orders_cstm`.`devchangenoteno_c` AS `devchangenoteno_c`,\
    `sales_orders_cstm`.`developmentworkreqd_c` AS `developmentworkreqd_c`,\
    SUBSTRING(`sales_orders_cstm`.`devworknotes_c`, 1,1024) AS `devworknotes_c`,\
    `sales_orders_cstm`.`devworkpromiseddate_c` AS `devworkpromiseddate_c`,\
    `sales_orders`.`discount_before_taxes` AS `discount_before_taxes`,\
    `sales_orders`.`due_date` AS `due_date`,\
    `users`.`employee_status` AS `employee_status`,\
    `sales_orders`.`exchange_rate` AS `exchange_rate`,\
    `users`.`first_name` AS `first_name`,\
    `sales_orders_cstm`.`freeofchargeorder_c` AS `freeofchargeorder_c`,\
    `sales_orders`.`gross_profit_so` AS `gross_profit_so`,\
    `sales_orders`.`gross_profit_so_usd` AS `gross_profit_so_usd`,\
    `sales_orders`.`id` AS `id`,\
    `sales_orders_cstm`.`id_c` AS `id_c`,\
    `users`.`in_directory` AS `in_directory`,\
    `sales_orders_cstm`.`interface_technical_complexity_c` AS `interface_technical_complexity_c`,\
    `sales_orders_cstm`.`interfacecontact_c` AS `interfacecontact_c`,\
    `sales_orders_cstm`.`interfaceduedate_c` AS `interfaceduedate_c`,\
    `sales_orders_cstm`.`interfaceorderstatus_c` AS `interfaceorderstatus_c`,\
    `sales_orders_cstm`.`interfacesassignedto_c` AS `interfacesassignedto_c`,\
    `sales_orders_cstm`.`interfacestallreason_c` AS `interfacestallreason_c`,\
    `sales_orders_cstm`.`interfacestartworkdate_c` AS `interfacestartworkdate_c`,\
    SUBSTRING(`sales_orders_cstm`.`internalnotes_c`,1,1024) AS `internalnotes_c`,\
    `sales_orders_cstm`.`invoicable_c` AS `invoicable_c`,\
    `accounts`.`invoice_as` AS `invoice_as`,\
    `sales_orders_cstm`.`invoicedate_c` AS `invoicedate_c`,\
    `sales_orders_cstm`.`invoicenum_c` AS `invoicenum_c`,\
    `users`.`is_admin` AS `is_admin`,\
    `users`.`is_group` AS `is_group`,\
    `accounts`.`last_activity_date` AS `last_activity_date`,\
    `users`.`last_login_attempt` AS `last_login_attempt`,\
    `users`.`last_name` AS `last_name`,\
    `sales_orders_cstm`.`licence_agreement_updated_c` AS `licence_agreement_updated_c`,\
    `sales_orders_cstm`.`licenceagreementupdated_c` AS `licenceagreementupdated_c`,\
    `accounts`.`lifetime_revenue` AS `lifetime_revenue`,\
    `users`.`local_extension` AS `local_extension`,\
    `users`.`location` AS `location`,\
    `users`.`login_attempts` AS `login_attempts`,\
    `sales_orders_cstm`.`mainproduct_c` AS `mainproduct_c`,\
    `users`.`messenger_id` AS `messenger_id`,\
    `users`.`messenger_type` AS `messenger_type`,\
    `sales_orders`.`modified_user_id` AS `modified_user_id`,\
    `sales_orders`.`name` AS `name`,\
    `users`.`need_new_password` AS `need_new_password`,\
    `sales_orders_cstm`.`neworexistingsystem_c` AS `neworexistingsystem_c`,\
    `sales_orders_cstm`.`old4sordernum_c` AS `old4sordernum_c`,\
    `sales_orders`.`opportunity_id` AS `opportunity_id`,\
    `sales_orders_cstm`.`ordercancelled_c` AS `ordercancelled_c`,\
    `sales_orders_cstm`.`otherstallreason_c` AS `otherstallreason_c`,\
    `sales_orders_cstm`.`partialinvoicedtotal_c` AS `partialinvoicedtotal_c`,\
    `sales_orders`.`partner_id` AS `partner_id`,\
    `accounts`.`payment_processor_id` AS `payment_processor_id`,\
    `users`.`personal_info_source` AS `personal_info_source`,\
    `accounts`.`phone_alternate__raw` AS `phone_alternate__raw`,\
    `users`.`phone_fax__raw` AS `phone_fax__raw (users)`,\
    `accounts`.`phone_fax__raw` AS `phone_fax__raw`,\
    `users`.`phone_home` AS `phone_home`,\
    `users`.`phone_home__raw` AS `phone_home__raw`,\
    `users`.`phone_mobile` AS `phone_mobile`,\
    `users`.`phone_mobile__raw` AS `phone_mobile__raw`,\
    `accounts`.`phone_office__raw` AS `phone_office__raw`,\
    `users`.`phone_other` AS `phone_other`,\
    `users`.`phone_other__raw` AS `phone_other__raw`,\
    `users`.`phone_work` AS `phone_work`,\
    `users`.`phone_work__raw` AS `phone_work__raw`,\
    `accounts`.`photo_filename` AS `photo_filename (accounts)`,\
    `users`.`photo_filename` AS `photo_filename`,\
    `users`.`photo_thumb` AS `photo_thumb (users)`,\
    `accounts`.`photo_thumb` AS `photo_thumb`,\
    `users`.`portal_only` AS `portal_only`,\
    `accounts`.`pp_customer_id` AS `pp_customer_id`,\
    `sales_orders`.`prefix` AS `prefix`,\
    `sales_orders`.`pretax` AS `pretax`,\
    `sales_orders`.`pretax_usd` AS `pretax_usd`,\
    `sales_orders_cstm`.`previousquotenum_c` AS `previousquotenum_c`,\
    `sales_orders`.`pricebook_id` AS `pricebook_id`,\
    `sales_orders_cstm`.`priority_c` AS `priority_c`,\
    SUBSTRING(`sales_orders_cstm`.`priorityexplanation_c`,1, 1024) AS `priorityexplanation_c`,\
    `sales_orders_cstm`.`progress_reported_via_kanban_c` AS `progress_reported_via_kanban_c`,\
    `users`.`project_mode` AS `project_mode`,\
    `sales_orders`.`purchase_order_num` AS `purchase_order_num`,\
    `users`.`quotation_mode` AS `quotation_mode`,\
    `users`.`receive_case_notifications` AS `receive_case_notifications`,\
    `users`.`receive_notifications` AS `receive_notifications`,\
    `users`.`recovery_ip_addr` AS `recovery_ip_addr`,\
    `users`.`recovery_key` AS `recovery_key`,\
    `users`.`recovery_key_time` AS `recovery_key_time`,\
    `sales_orders`.`related_quote_id` AS `related_quote_id`,\
    `sales_orders_cstm`.`relatedcasenum_c` AS `relatedcasenum_c`,\
    `users`.`reports_to_id` AS `reports_to_id`,\
    SUBSTRING(`accounts`.`sales_popup`, 1, 1024) AS `sales_popup`,\
    `users`.`salutation` AS `salutation`,\
    SUBSTRING(`accounts`.`service_popup`, 1, 1024) AS `service_popup`,\
    `users`.`sf_id` AS `sf_id (users)`,\
    `accounts`.`sf_id` AS `sf_id`,\
    `sales_orders`.`shipping_account_id` AS `shipping_account_id`,\
    `sales_orders`.`shipping_address_city` AS `shipping_address_city`,\
    `sales_orders`.`shipping_address_country` AS `shipping_address_country`,\
    `accounts`.`shipping_address_countrycode` AS `shipping_address_countrycode (accounts)`,\
    `sales_orders`.`shipping_address_countrycode` AS `shipping_address_countrycode`,\
    `sales_orders`.`shipping_address_postalcode` AS `shipping_address_postalcode`,\
    `sales_orders`.`shipping_address_state` AS `shipping_address_state`,\
    `accounts`.`shipping_address_statecode` AS `shipping_address_statecode (accounts)`,\
    `sales_orders`.`shipping_address_statecode` AS `shipping_address_statecode`,\
    `sales_orders`.`shipping_address_street` AS `shipping_address_street`,\
    `sales_orders`.`shipping_contact_id` AS `shipping_contact_id`,\
    `sales_orders`.`shipping_provider_id` AS `shipping_provider_id`,\
    `sales_orders`.`show_components` AS `show_components`,\
    `sales_orders`.`show_list_prices` AS `show_list_prices`,\
    `users`.`signature_image_filename` AS `signature_image_filename`,\
    `users`.`skype_id` AS `skype_id`,\
    `users`.`sms_address` AS `sms_address`,\
    `sales_orders`.`so_number` AS `so_number`,\
    `sales_orders`.`so_stage` AS `so_stage`,\
    `users`.`status` AS `status`,\
    `sales_orders_cstm`.`strategicimportance_c` AS `strategicimportance_c`,\
    `accounts`.`stripe_customer_id` AS `stripe_customer_id`,\
    `sales_orders`.`subtotal` AS `subtotal`,\
    `sales_orders`.`subtotal_usd` AS `subtotal_usd`,\
    `users`.`sugar_login` AS `sugar_login`,\
    `accounts`.`tax_code_id` AS `tax_code_id`,\
    `accounts`.`tax_exempt` AS `tax_exempt (accounts)`,\
    `sales_orders`.`tax_exempt` AS `tax_exempt`,\
    `sales_orders`.`tax_information` AS `tax_information`,\
    `sales_orders`.`terms` AS `terms`,\
    `users`.`title` AS `title`,\
    `sales_orders`.`tracking_reference` AS `tracking_reference`,\
    `users`.`user_hash` AS `user_hash`,\
    `users`.`user_name` AS `user_name`,\
    SUBSTRING(`users`.`user_preferences`, 1, 1024) AS `user_preferences`,\
    `users`.`created_by` AS `users_created_by`,\
    `users`.`date_entered` AS `users_date_entered`,\
    `users`.`date_modified` AS `users_date_modified`,\
    `users`.`deleted` AS `users_deleted`,\
    SUBSTRING(`users`.`description`, 1, 1024) AS `users_description`,\
    `users`.`email1` AS `users_email1`,\
    `users`.`email2` AS `users_email2`,\
    `users`.`id` AS `users_id`,\
    `users`.`modified_user_id` AS `users_modified_user_id`,\
    `users`.`phone_fax` AS `users_phone_fax`,\
    `users`.`website` AS `website`,\
    `users`.`week_start_day` AS `week_start_day`,\
    `accounts`.`woo_id` AS `woo_id (accounts)`,\
    `sales_orders`.`woo_id` AS `woo_id`,\
    `accounts`.`woo_locked` AS `woo_locked (accounts)`,\
    `sales_orders`.`woo_locked` AS `woo_locked`,\
    `sales_orders`.`woo_order_stage` AS `woo_order_stage`,\
    `sales_orders_cstm`.`workinprogresspercentcomplete_c` AS `workinprogresspercentcomplete_c`,\
    `sales_orders_cstm`.`xxtest_c` AS `xxtest_c`\
  FROM `sales_orders`\
    INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
    INNER JOIN `accounts` ON (`sales_orders`.`shipping_account_id` = `accounts`.`id`)\
    LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`)"
                    )   
  number_of_records = len(cur.fetchall())
  for r in cur.fetchall():
      dicts = [{'Sales_Order_No':r['so_number'], 'Date_entered' : r['date_entered']}] #'Order_value_Excl_VAT': r['subtotal_usd'],
      print(dicts)
  # for d in dicts:
                                
  #         app_tables.tableau.add_row(**d)
  
  # number_of_records = len(dicts)
  return  dicts, number_of_records