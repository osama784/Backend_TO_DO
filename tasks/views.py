from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import status


from .models import Task, Category
from .serializers import TaskSerializerShow, TaskSerializerCreate, CategorySerializer


from api.permissions import IsOwner



"""
Tasks:
"""

class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerShow
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        data = {
            'owner': request.user.username,
            'tasks': serializer.data,
            
        }
        return Response(data)


    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        qs = qs.filter(owner=request.user)
        
        category = request.GET.get('q_category')
        is_done = request.GET.get('q_done')
        sort = request.GET.get('q_sort')

        if is_done == "True" or is_done == "False":
            is_done = True if is_done == "True" else False 
            qs = qs.filter(is_done=is_done)
        
        try:
            if Category.objects.filter(id=category).exists():
                qs = qs.filter(category = category)
        except ValueError:
            pass

        if sort == 'old':
            qs = qs.filter.order_by('created')
        return qs
    

list_tasks = TaskListAPIView.as_view()



class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerCreate
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.pk
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = serializer.instance
        serializer = TaskSerializerShow(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

create_task = TaskCreateAPIView.as_view()    



class TaskDeleteAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerShow
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        detail = {
            'detail': 'Task deleted.'
        }
        return Response(detail, status=status.HTTP_204_NO_CONTENT)

delete_task = TaskDeleteAPIView.as_view()    


class TaskUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerCreate
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        data = request.data.copy()
        data['owner'] = request.user.pk
        print(data)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = serializer.instance
        serializer = TaskSerializerShow(instance)
        return Response(serializer.data)

update_task = TaskUpdateAPIView.as_view()    



"""
Categories:
"""

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        data = {
            'tasks_number': Task.objects.filter(owner=request.user).count(),
            'categories': serializer.data,
            
        }
        return Response(data)

    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        qs = qs.filter(owner=request.user)
        return qs
    
    
list_category = CategoryListAPIView.as_view()


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

create_category = CategoryCreateAPIView.as_view()


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        detail = {
            'detail': 'Category deleted.'
        }
        return Response(detail, status=status.HTTP_204_NO_CONTENT)


delete_category = CategoryDeleteAPIView.as_view()


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['owner'] = request.user.pk
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer) 

        return Response(serializer.data)

update_category = CategoryUpdateAPIView.as_view()