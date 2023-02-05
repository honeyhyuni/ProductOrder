from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import GetProductSerializers, NGetProductSerializers, GetLoginProductSerializers


class ProductAPIView(ModelViewSet):
    """
        Product CRUD
    """
    queryset = Product.objects.all()
    serializer_class = GetProductSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes_by_action = {
        'get': (IsAuthenticatedOrReadOnly,),
        'nGet': (IsAdminUser,)
    }
    serializer_classes = {
        'LoginUser': GetLoginProductSerializers,
        'get': GetProductSerializers,
        'nGet': NGetProductSerializers,
    }

    """
        Get permission -> IsAuthenticatedOrReadOnly
        Not Get('POST', PUT, PATCH, DELETE) permission -> IsAdminUser
    """
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = self.permission_classes_by_action['get']
        self.permission_classes = self.permission_classes_by_action['nGet']
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['like'] = self.request
        return context


    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return self.serializer_classes['get']
        if self.action == 'list' or self.action == 'retrieve':
            return self.serializer_classes['LoginUser']
        return self.serializer_classes['nGet']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def perform_update(self, serializer):
        serializer.save()

    """
        좋아요, 좋아요 취소 API
    """
    @action(detail=True, methods=["POST"])
    def like(self, request, pk):
        product = self.get_object()
        product.like_user_set.add(self.request.user)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, pk):
        product = self.get_object()
        product.like_user_set.remove(self.request.user)
        return Response(status.HTTP_204_NO_CONTENT)
