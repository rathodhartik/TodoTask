from .import views
from django.urls import path

urlpatterns = [
    path('signin', views.sign_in.as_view(),name='signinAPI'),
    path('callback', views.callback.as_view(),name='callback'),
    path('task_exportAPI', views.task_exportAPI.as_view(),name='task_exportAPI'),
    path('tasks_SYNC_API', views.tasks_SYNC_API.as_view(),name='tasks_SYNC_API'),
    
    path('AddTAskAPI', views.AddTAskAPI.as_view(),name='AddTAskAPI'),
    path('DeleteAskAPI/<int:id>/', views.DeleteAskAPI.as_view(),name='DeleteAskAPI'),
    path('updateAskAPI/<int:id>/', views.updateAskAPI.as_view(),name='updateAskAPI'),
    path('usergetAPI', views.usergetAPI.as_view(),name='usergetAPI'),

]
