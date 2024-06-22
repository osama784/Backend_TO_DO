from rest_framework import serializers

from .models import Task, Category


class TaskSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    task_number = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = "__all__"

    def get_task_number(self, obj):
        count = obj.task_set.count()    
        return count


class TaskSerializerShow(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    category = CategorySerializer()
    class Meta:
        model = Task
        fields = '__all__'
