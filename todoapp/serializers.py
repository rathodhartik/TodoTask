from rest_framework import serializers
from .models import *

class TaskDetailsSerializers(serializers.ModelSerializer):
    class Meta:
      model = TaskDetails
      fields = "__all__"
      
      
    def update(self, instance, validated_data): 
      instance.task = validated_data.get('task', instance.task)
      instance.status = validated_data.get('status', instance.status)
      instance.due_date = validated_data.get('due_date', instance.due_date)
      instance.save()
      return instance