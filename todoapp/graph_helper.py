import requests
import json
from django.template.loader import get_template

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
  user = requests.get(
    '{0}/me'.format(graph_url),
    headers={
      'Authorization': 'Bearer {0}'.format(token)
    },
    params={
      '$select': 'displayName,mail,mailboxSettings,userPrincipalName'
    })
  return user.json()
  
def get_task_list(token):
  headers = {
    
    'Authorization': 'Bearer {0}'.format(token)
   
  }
  events = requests.get('{0}/me/todo/lists'.format(graph_url),
    headers=headers)
  return events.json()
  
  
def get_task(token,todo_id):
  headers = {
    'Authorization': 'Bearer {0}'.format(token),
  }
  events = requests.get('{0}/me/todo/lists/{1}/tasks'.format(graph_url,todo_id),
    headers=headers)
  return events.json()


def create_task(token,todo_id,data,status_,task_data):
  ctx={
    "user_data":task_data
  }
  usr_message = get_template('task.html').render(ctx)

  new_event={
     "title":data['task']['text'],
     "status":status_,
    "dueDateTime": {
      "dateTime":  data['due_date'],
      "timeZone": 'Asia/Kolkata'
     },
    'reminderDateTime': {
      'dateTime':  data['start_date'],
      'timeZone': 'Asia/Kolkata'
      },
    "body":{
      'contentType': 'html',
      'content':usr_message
      }
    }
  headers = {
      'Authorization': 'Bearer {0}'.format(token),
      'Content-Type':'application/json',
    }
  try:
      events_task=requests.post('{0}/me/todo/lists/{1}/tasks'.format(graph_url,todo_id),
                    headers=headers,
                    data=json.dumps(new_event))
      return events_task.json()
  except Exception as e:
      print(e)



def task_deleted(token,todo_id,todo_task_id):
  headers = {
    'Authorization': 'Bearer {0}'.format(token),
  }
  requests.delete('{0}/me/todo/lists/{1}/tasks/{2}'.format(graph_url,todo_id,todo_task_id),
    headers=headers)
  
  return "success"



def task_update(token,todo_id,todo_task_id,data,status_):
  new_event={
     "title":data['task'],
     "status":status_,
     "dueDateTime": {
      "dateTime":  data['due_date'],
      "timeZone": 'Asia/Kolkata'
     },
    }

  headers = {
      'Authorization': 'Bearer {0}'.format(token),
      'Content-Type':'application/json',
    }
  try:
      events_task=requests.patch('{0}/me/todo/lists/{1}/tasks/{2}'.format(graph_url,todo_id,todo_task_id),
                    headers=headers,
                    data=json.dumps(new_event))
      data=events_task.json()
      print(data)
      return "success"
  except Exception as e:
      print(e)
      return False
      
      

def task_update1(token,todo_id,todo_task_id,data,status_):
  new_event={
     "title":data['task'],
     "status":status_,
     "dueDateTime": {
      "dateTime":  data['due_date'],
      "timeZone": 'Asia/Kolkata'
     },
    }

  headers = {
      'Authorization': 'Bearer {0}'.format(token),
      'Content-Type':'application/json',
    }
  try:
      events_task=requests.patch('{0}/me/todo/lists/{1}/tasks/{2}'.format(graph_url,todo_id,todo_task_id),
                    headers=headers,
                    data=json.dumps(new_event))
      data=events_task.json()
      print(data,"....................")
      return "success"
  except Exception as e:
      print(e)
      return False
      

