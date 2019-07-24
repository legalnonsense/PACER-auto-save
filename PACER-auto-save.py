#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from googleapiclient import discovery
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import os
import re
import base64
import html

def save_pdf_attachment(request_id, response, exception):
    if exception is not None:
        print('messages.get failed for message id {}: {}'.format(request_id, exception))
    else:
        for part in response['payload']['parts'][1:]:
            if part['mimeType'] == 'application/pdf':
                attachment_id = part['body']['attachmentId']
                message_id = m['id']

                # try:
                    
                #     filename = (re.search(r'(.+?\sv\.\s.+?)\s(?:.+?Docket\sentry\snumber\:\s\d+[^\s]+\s)(.+)', response['snippet']).group(1) 
                #                 + " - "
                #                 + re.search(r'\[dckt\s(\d+_\d+)\]', part['filename']).group(1)
                #                 + " - "
                #                 + re.search(r'(.+?\sv\.\s.+?)\s(?:.+?Docket\sentry\snumber\:\s\d+[^\s]+\s)(.+)', response['snippet']).group(2))
                # except:
                #     try:
                #         filename = (re.search(r'(.+?\sv\.\s.+?)\s(?:.+?Docket\sentry\snumber\:\s\d+[^\s]+\s)(.+)', response['snippet']).group(1) 
                #                     + " - "
                #                     + re.search(r'\[dckt\s(\d+_\d+)\]', part['filename']).group(1))
                #     except:
                #         filename = response['snippet'].split(' ')[0] + ' _ ' + part['filename']
                        
                    
                # filename = html.unescape(filename[:150])

                # #filename = filename.replace('(', '')
                # #filename = filename.replace(')', '')

                # filename = filename.strip() + '.pdf'


                filename = response['snippet'].split(' ')[0] + ' _ ' + part['filename']
                
                attachment=GMAIL.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute() 
                #print("message_id: {}; filename: {}; attachment_id: {}".format(message_id, filename, attachment_id))

                if (filename and attachment):
                    # this will write the attachment to a file
                    with open (PATH + filename, 'wb') as f:
                        print("Saved file: {}".format( PATH+ filename))
                        f.write(base64.urlsafe_b64decode(attachment['data'].encode('UTF-8')))

                filename = ''
                attachment = None 
                        
PATH = "/home/jeff/Cases/Dockets/"
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage(os.path.expanduser('~/.config/i3/py3status/token.json'))
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(os.path.expanduser('~/.config/i3/py3status/credentials.json'), SCOPES)
    creds = tools.run_flow(flow, store)

http = Http()    
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

# this will get a list of messages, which will will return a list of messages matching the search
message_list=GMAIL.users().messages().list(userId='me', q='from:ECFdocuments@pacerpro.com is:unread').execute()
#message_list_api=GMAIL.users().messages()
message_list_req = message_list_api.list(userId='me', q='from:ECFdocuments@pacerpro.com')

while message_list_req is not None:
    gmail_msg_list = message_list_req.execute()
    batch = GMAIL.new_batch_http_request(callback=save_pdf_attachment)

    for m in gmail_msg_list['messages']: 

        batch.add(GMAIL.users().messages().get(userId='me', id=m['id'], format='full'), request_id=m['id'])

    batch.execute(http=http)
            

    message_list_req = message_list_api.list_next(message_list_req, gmail_msg_list)
