#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from googleapiclient import discovery
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import os
import re
import base64


PATH = "/home/jeff/Cases/Dockets/"
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage(os.path.expanduser('~/.config/i3/py3status/token.json'))
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(os.path.expanduser('~/.config/i3/py3status/credentials.json'), SCOPES)
    creds = tools.run_flow(flow, store)

GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

# this will get a list of messages, which will will return a list of messages matching the search
#message_list=GMAIL.users().messages().list(userId='me', q='from:ECFdocuments@pacerpro.com is:unread').execute()
message_list=GMAIL.users().messages().list(userId='me', q='from:ECFdocuments@pacerpro.com').execute()
if message_list['resultSizeEstimate'] > 0:

    for m in message_list['messages']: 

        message = GMAIL.users().messages().get(userId='me', id=m['id'], format='full').execute()

        for part in message['payload']['parts'][1:]:

            if part['mimeType'] == 'application/pdf':
                attachment_id = part['body']['attachmentId']
                message_id = m['id']
                filename = message['snippet'].split(' ')[0] + ' _ ' + part['filename']
                attachment=GMAIL.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute() 
if message_list['resultSizeEstimate'] > 0:

    for m in message_list['messages']: 

        message = GMAIL.users().messages().get(userId='me', id=m['id'], format='full').execute()

        for part in message['payload']['parts'][1:]:

            if part['mimeType'] == 'application/pdf':
                attachment_id = part['body']['attachmentId']
                message_id = id['id']
                filename = message['snippet'].split(' ')[0] + ' _ ' + re.search(r'(\[dckt \d+_\d*\])', filename).group(0) + " _ " + re.search(r'(.+?)\[', filename).group(1).strip()
                attachment=GMAIL.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute() 

                #print("message_id: {}; filename: {}; attachment_id: {}".format(message_id, filename, attachment_id))
            
                # this will write the attachment to a file
                with open (PATH + filename, 'wb') as f:
                    f.write(base64.urlsafe_b64decode(attachment['data'].encode('UTF-8')))

            
                # this will write the attachment to a file
                with open (PATH + filename, 'wb') as f:
                    f.write(base64.urlsafe_b64decode(attachment['data'].encode('UTF-8')))

                print("Saved file: {}".format( PATH+ filename))
