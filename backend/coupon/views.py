from collections import OrderedDict
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Coupon, CouponRules, UserCoupon
from .serializers import CouponListCreateSerializers, CouponRuleListSerializers, \
    CreateUserCouponSerializers
from django.core.exceptions import ObjectDoesNotExist


class PostPageNumberPagination(PageNumberPagination):
    page_size = 10
    """
        Default page_size = 10
        return (data, pageCnt(전체 페이지 수), curPage(현재 페이지))
    """

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


class CreateListCoupon(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponListCreateSerializers
    permission_classes = (AllowAny,)
    pagination_class = PostPageNumberPagination
    """
          GET -> coupon List
          Post -> Create coupon
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AllCouponRulesList(APIView):
    permission_classes = (AllowAny,)
    """
        Get -> CouponRules List
    """

    def get(self, request, *args, **kwargs):
        couponRulesList = CouponRules.objects.all()

        data = {
            'couponRulesList': couponRulesList,
        }
        serializer = CouponRuleListSerializers(instance=data)
        return Response(serializer.data)


class UserCouponAPIView(ListCreateAPIView):
    """
        GET -> 로그인 한 User 의 쿠폰 List
        POST -> 로그인한 User 에게 쿠폰 부여 Coupon_rules 는 선택해야함
    """
    queryset = UserCoupon.objects.all()
    permission_classes = (AllowAny,)
    # pagination_class = PostPageNumberPagination
    serializer_class = CreateUserCouponSerializers
    # serializer_classes = {
    #     'list': UserCouponListSerializers,
    #     'create': CreateUserCouponSerializers
    # }

    # def get_serializer_class(self, *args, **kwargs):
    #     if self.request.method == "POST":
    #         return self.serializer_classes['create']
    #     return self.serializer_classes['list']

    def get_queryset(self):
        return UserCoupon.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
            User가 선택한 쿠폰의 active = True 인 객체를 하나 꺼내온후
            active 를 False 로 바꾸고 User에게 쿠폰을 부여한다.
        """
        temp_coupon = Coupon.objects.filter(coupon_rules=self.request.data['coupon.coupon_rules']).filter(
            active=True).first()

        if temp_coupon is None:
            return Response("this Type haven't Coupon", status=status.HTTP_404_NOT_FOUND)

        context = {'user': self.request.user, 'coupon': temp_coupon}

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()