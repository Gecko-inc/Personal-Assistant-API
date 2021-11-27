from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from finance.models import Expenses, Category
from finance.serializer import ExpensesSerializer


class ExpensesView(APIView):
    @swagger_auto_schema(tags=['Finance'])
    def get(self, request):
        user = request.user
        return Response(ExpensesSerializer(Expenses.objects.filter(user=user), many=True).data, status=200)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['category_id', "money", 'title'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                 'money': openapi.Schema(type=openapi.TYPE_STRING),
                             },
                         ),
                         )
    @transaction.atomic
    def post(self, request):
        sid = transaction.savepoint()
        user = request.user
        data = request.data
        try:
            money = float(data.get("money"))
        except (ValueError, TypeError):
            return Response({"error": "Invalid data"}, status=400)

        try:
            category = Category.objects.get(id=data.get("category_id"))
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=404)

        sid = transaction.savepoint()
        Expenses.objects.create(
            user=user,
            category_id=category.id,
            title=data.get("title"),
            money=money
        )
        if user.update_balance(money*-1) < 0:
            transaction.savepoint_rollback(sid)
            return Response({"error": "the balance cannot be negative"}, status=400)
        return Response(status=201)