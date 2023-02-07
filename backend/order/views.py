from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from coupon.views import PostPageNumberPagination
from order.serializers import OrderListRetrieveSerializer
from order.models import Order


class OrderListAPIView(ListAPIView):
    """
        주문 내역 List API View
    """
    queryset = Order.objects.all()
    serializer_class = OrderListRetrieveSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderRetrieveAPIView(RetrieveAPIView):
    """
        주문 내역 상세 APIView
    """
    queryset = Order.objects.all()
    serializer_class = OrderListRetrieveSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
