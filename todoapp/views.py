from .models import TASK_STATUS, TaskDetails
from todoapp.serializers import TaskDetailsSerializers
from todoapp.utilities import *
from todoapp.graph_helper import *
from rest_framework.response import Response
from rest_framework.views import APIView
from pprint import pprint
from django.shortcuts import redirect
from TodoTask.settings import *
import datetime

client = ConfidentialClientApplication(client_id=app_id,client_credential=client_secret)


class sign_in(APIView):
    def get(self, request):
        authorization_url=client.get_authorization_request_url(SCOPES)
        url=redirect(authorization_url)
        data={
        "url":url.url
        }
        return Response(data)

class callback(APIView):
    def get(self, request):
        data=request.META['QUERY_STRING']
        authorization_code=data.split("=")
        access_token = client.acquire_token_by_authorization_code(code=authorization_code[1],scopes=SCOPES)
        token={
        "msg":"token get",
        "token":access_token
        }
        return Response(token)
    


class usergetAPI(APIView):
  def get(self, request):
    token=request.data["access_token"]
    data=get_user(token)
    return Response(data)
    
class AddTAskAPI(APIView):
  def get(self, request):
      user=request.user
      cat = TaskDetails.objects.all()
      serializer = TaskDetailsSerializers(cat,many=True,context={'user':user})
      return Response(serializer.data)

  def post(self, request):
    user=request.user
    data=request.data
    serializer = TaskDetailsSerializers(data=data,context={'user':user})
    if serializer.is_valid():
      serializer.save()
      return Response(success_added("successfully added",serializer.data),status=CREATED)
    else:
      return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)

class DeleteAskAPI(APIView):
  def delete(self, request,id):
    token=request.data["access_token"]
    events = get_task_list(token)
    todo_id=events['value'][0]['id']
    task_dlt=TaskDetails.objects.get(id=id)
    todo_task_id=task_dlt.todo_task_id
    print(todo_id,todo_task_id)
    staus=task_deleted(token,todo_id,todo_task_id)
    if staus=="success":  
      task_dlt.delete()
      return Response(success_deleted("Task Successfully Deleted",""),status=OK)
    
class updateAskAPI(APIView):
  def patch(self, request,id):
    data = request.data
    token=request.data["access_token"]
    events = get_task_list(token)
    todo_id=events['value'][0]['id']
    Emp1 = TaskDetails.objects.get(id=id)
    todo_task_id=Emp1.todo_task_id
    serializer = TaskDetailsSerializers(Emp1, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        data=serializer.data
        status_ = dict(TASK_STATUS).get(data["status"])
        print(data['task'])
        status=task_update(token,todo_id,todo_task_id,data,status_)
        if status=="success":        
          return Response(success_added("Data Updated Successfully!",serializer.data),status=OK)
        else:
          return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)

  
class task_exportAPI(APIView):
    def post(self, request):
      t_id=request.data['t_id']
      token=request.data["access_token"]
      user = get_user_list(token)
      print(user,".......................")
      events = get_task_list(token)
      todo_id=events['value'][0]['id']
      for ta in t_id:
        list = TaskDetails.objects.get(id=ta)
        todo_task_id=list.todo_task_id
        serializer = TaskDetailsSerializers(list)
        user_data=serializer.data
        task_data={user_data["id"] : user_data['text'] for user_data in user_data['task']['task_comp'][0]['task_recom']}
        try:
          events = get_task(token,todo_id)
          status_ = dict(TASK_STATUS).get(user_data["status"])
          for event_data in events['value']:
            # if user_data['task']['text']==event_data['title']:
            if user_data['todo_task_id']==event_data['id']:
              task_update=task_update1(token,todo_id,todo_task_id,user_data,status_)
              if task_update=="success":
                print("Todo task updated.")
              break
          else:    
            task=create_task(token,todo_id,user_data,status_,task_data)
            print(task)
            task_id=task['id']
            get_user=TaskDetails.objects.get(task=user_data['task'])
            get_user.todo_task_id=task_id
            get_user.exported=True
            get_user.save()
            print("Task created")
        except Exception as e:
          print(e)
          return Response(data_fail("Data Invalid",serializer.errors),status=BAD_REQUEST)
      return Response(success_added("successfully export",""),status=CREATED)

  
class tasks_SYNC_API(APIView):
    def post(self, request):
        token=request.data["access_token"]
        events = get_task_list(token)
        todo_id=events['value'][0]['id']
        events = get_task(token,todo_id)
        print(events['value'])
        for events_data in events['value']:
          try:
            user_data=TaskDetails.objects.get(todo_task_id=events_data['id'])
            task_st=[TASK_STATUS[c][0] for c in range(len(TASK_STATUS)) if events_data['status']==TASK_STATUS[c][1]]
            print(task_st)
            # user_data.task=events_data['title']
            user_data.status=task_st[0]
            user_data.due_date=str(events_data['dueDateTime']['dateTime'])
            user_data.save()
          except Exception as e:
            user_data=None
        return Response(success_added("Successfully SYNC",""),status=CREATED)



