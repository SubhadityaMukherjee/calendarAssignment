import datetime
from datetime import date
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def calendar_entry(text,dat):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    evp = datetime.datetime.strptime(dat+'/{}'.format(date.today().year), '%d/%m/%Y')
    ev = str(evp).split(' ')[0]+'T03:00:00-07:00'
    ev2 =str(evp).split(' ')[0]+'T09:00:00-05:00'


    event = {
    'summary': text,
    'start':{
        'dateTime':str(ev),
    },
    'end':{
        'dateTime':str(ev2),
    },

    }
    # print(event)
    event = service.events().insert(calendarId='primary', body=event).execute()



def actually_add():
    with open('deadlines.txt','r') as f:
        p = f.readlines()
        for a in p:
            curr = a.split(' ')
            dat = curr[-1].strip()
            curr[-1] = ''
            stri = ' '.join(curr).strip()

            # print(curr,stri)
            calendar_entry(stri,dat)

print('[INFO] Enter your deadlines in the format description day/month\n')
actually_add()
