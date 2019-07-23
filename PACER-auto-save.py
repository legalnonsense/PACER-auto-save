#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from googleapiclient import discovery
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import os
import base64



SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage(os.path.expanduser('~/.config/i3/py3status/token.json'))
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(os.path.expanduser('~/.config/i3/py3status/credentials.json'), SCOPES)
    creds = tools.run_flow(flow, store)

GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))






# this will get a list of messages, which will will return a list of messages matching the search
messages=GMAIL.users().messages().list(userId='me', q='from:ECFdocuments@pacerpro.com is:unread', format='full').execute()

# ['messages'][0]['id'] will get the message ID 

# this will get the specific message
message=GMAIL.users().messages().get(userId='me', id='MESSAGE ID', format='full').execute()

# this will get the attachment
attachment=GMAIL.users().messages().attachments().get(userId='me', messageId='MESSAGE ID', id='ATTACHMENT ID').execute() 

#figure out the file name

#figure out the path 


# this will write the attachment to a file
with open ("PATH", 'wb') as f:
    f.write(base64.urlsafe_b64decode(attachment['data'].encode('UTF-8')))





    
