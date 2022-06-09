import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
import os.path

import requests
from requests_kerberos import HTTPKerberosAuth
import urllib3
import pandas as pd
import json


def download_query():
	# # this is to ignore the ssl insecure warning as we are passing in 'verify=false'
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
 
	headers = { 'Content-type': 'application/json' }
	# Replace the ID here with the query ID you want to pull
	# Note: the query ID must be a valid ID
	url = 'https://hsdes-api.intel.com/rest/query/execution/1509292211'
	response = requests.get(url, verify=False, auth=HTTPKerberosAuth(), headers = headers)

	if (response.status_code == 200):
		data_rows = response.json()['data']
		index = 1
		df = pd.DataFrame()

		for row in data_rows:
			# Note: you can pull any field thats defined in the query select list
			#print(row['id'])
			# import pdb;pdb.set_trace()
			# json_str = json.dumps(response.json()['data'])
			# df_json = pd.read_json(json_str)
			df = df.append(pd.DataFrame(row, index=[index]))
			index += 1
			
			 

		#df.to_excel('All_WWAN_OPEN_issues(FIBC_FAE_tag).xlsx')
		print("Download Complete!")
		return df



def intel_email_send_notempty(attachment_location = ''):
	try:
		content = MIMEMultipart()  #建立MIMEMultipart物件
		content["subject"] = "[Intel]FIBC_FAE daily issue report"  #郵件標題
		content["from"] = "lulu.chang@intel.com"  #寄件者
		content["to"] = "PC_FAE@fibocom.com, sam.hsu@intel.com, chung.luan@intel.com" #收件者
		content["cc"] = "lulu.chang@intel.com"
		content.attach(MIMEText("FIBC_FAE daily issue report"))  #郵件內容
	
		if attachment_location != '':
			filename = os.path.basename(attachment_location)
			attachment = open(attachment_location, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(attachment.read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
			content.attach(part)

		server = smtplib.SMTP('mail.intel.com')
		server.send_message(content)
		server.quit()
		print("Send Complete!")
		return 0
	except Exception as e:
		print(e)
		return -1

def intel_email_send_empty():
	try:
		content = MIMEMultipart()  #建立MIMEMultipart物件
		content["subject"] = "[Intel]FIBC_FAE daily issue report"  #郵件標題
		content["from"] = "lulu.chang@intel.com"  #寄件者
		content["to"] = "PC_FAE@fibocom.com, sam.hsu@intel.com, chung.luan@intel.com" #收件者
		content["cc"] = "lulu.chang@intel.com"
		content.attach(MIMEText("FIBC_FAE daily issue report: No ticket with FIBC_FAE tag today."))  #郵件內容
	
		# if attachment_location != '':
		# 	filename = os.path.basename(attachment_location)
		# 	attachment = open(attachment_location, "rb")
		# 	part = MIMEBase('application', 'octet-stream')
		# 	part.set_payload(attachment.read())
		# 	encoders.encode_base64(part)
		# 	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		# 	content.attach(part)

		server = smtplib.SMTP('mail.intel.com')
		server.send_message(content)
		server.quit()
		print("Send Complete!")
		return 0
	except Exception as e:
		print(e)
		return -1

if __name__ == "__main__":

    #download kpi query
    df = download_query()
    fname = "All_WWAN_OPEN_issues(FIBC_FAE_tag).xlsx"
    df.to_excel(fname)
    if df.empty == True:
    	print("no tickets!")
    	intel_email_send_empty()
    else:
    	intel_email_send_notempty('All_WWAN_OPEN_issues(FIBC_FAE_tag).xlsx')
    #intel_email_send('All_WWAN_OPEN_issues(HP MapleSpring).xlsx')

#download_query()
#time.sleep(5)
#intel_email_send('All_WWAN_OPEN_issues(FIBC_FAE_tag).xlsx')





