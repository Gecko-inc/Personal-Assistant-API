from django.db import transaction
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.views import init_user
from finance.models import Expenses, Category, Income
from finance.serializer import ExpensesSerializer, CategorySerializer, IncomeSerializer


class ExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Finance'])
    def get(self, request):
        user = init_user(request)
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
        user = init_user(request)
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
        if user.update_balance(money * -1) < 0:
            transaction.savepoint_rollback(sid)
            return Response({"error": "the balance cannot be negative"}, status=400)
        return Response(status=201)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['expense_id'],
                             properties={
                                 'expense_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                             },
                         ),
                         )
    def delete(self, request, **kwargs):
        user = init_user(request)
        try:
            Expenses.objects.get(id=request.data.get("expense_id"), user=user).delete()
        except Expenses.DoesNotExist:
            pass
        return Response(status=201)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['id'],
                             properties={
                                 'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                 'money': openapi.Schema(type=openapi.TYPE_STRING),
                             },
                         ),
                         )
    @transaction.atomic
    def put(self, request):
        data = request.data
        user = init_user(request)
        sid = transaction.savepoint()
        try:
            expenses = Expenses.objects.get(id=data.get("id"), user=user)
            expenses.title = data.get("title", expenses.title)
            if data.get("money"):
                user.update_balance(expenses.money)
            expenses.money = data.get("money", expenses.money)
            expenses.category_id = data.get("category_id", expenses.category_id)
            expenses.save()
            try:
                money = float(data.get("money"))
            except (ValueError, TypeError):
                return Response({"error": "Invalid data"}, status=400)

            if user.update_balance(money * -1) < 0:
                transaction.savepoint_rollback(sid)
                return Response({"error": "the balance cannot be negative"}, status=400)
            return Response(ExpensesSerializer(expenses, many=False).data, status=200)
        except Expenses.DoesNotExist:
            return Response({
                "error": "Expenses does not exist"
            }, status=404)


class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Finance'])
    def get(self, request):
        user = init_user(request)
        return Response(CategorySerializer(Category.objects.filter(Q(user=None) | Q(user=user)),
                                           many=True).data)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['title'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                             },
                         ),
                         )
    def post(self, request):
        user = init_user(request)
        category = Category.objects.create(title=request.data.get("title"), user=user)
        return Response(CategorySerializer(category, many=False).data, status=200)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['id'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                             },
                         ),
                         )
    def put(self, request):
        data = request.data
        user = init_user(request)
        try:
            category = Category.objects.get(id=data.get("id"), user=user)
            category.title = data.get("title", category.title)
            category.save()
            return Response(CategorySerializer(category, many=False).data, status=200)
        except Expenses.DoesNotExist:
            return Response({
                "error": "Category does not exist"
            }, status=404)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['category_id'],
                             properties={
                                 'category_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                             },
                         ),
                         )
    def delete(self, request, **kwargs):
        user = init_user(request)
        try:
            Expenses.objects.get(id=request.data.get("category_id"), user=user).delete()
        except Expenses.DoesNotExist:
            pass
        return Response(status=201)


class IncomeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Finance'])
    def get(self, request):
        user = init_user(request)
        return Response(IncomeSerializer(Income.objects.filter(user=user), many=True).data, status=201)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['title', 'money'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'money': openapi.Schema(type=openapi.TYPE_STRING),
                             },
                         ),
                         )
    def post(self, request):
        user = init_user(request)
        data = request.data
        try:
            money = float(data.get("money"))
        except (ValueError, TypeError):
            return Response({"error": "Invalid data"}, status=400)
        income = Income.objects.create(
            user=user,
            title=data.get("title"),
            money=money
        )
        user.update_balance(money)
        return Response(IncomeSerializer(income, many=False).data, status=201)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['id'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'money': openapi.Schema(type=openapi.TYPE_STRING),
                                 'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                             },
                         ),
                         )
    @transaction.atomic
    def put(self, request):
        user = init_user(request)
        data = request.data
        try:
            money = float(data.get("money"))
        except (ValueError, TypeError):
            return Response({"error": "Invalid data"}, status=400)
        sid = transaction.savepoint()
        try:
            income = Income.objects.get(id=data.get("id"), user=user)
            income.title = data.get("title", income.title)
            if data.get("money"):
                if user.update_balance(income.money * -1) < 0:
                    transaction.savepoint_rollback(sid)
                    return Response({"error": "the balance cannot be negative"}, status=400)

            income.money = money
            income.save()
            user.update_balance(money)
            return Response(CategorySerializer(income, many=False).data, status=200)
        except Expenses.DoesNotExist:
            transaction.savepoint_rollback(sid)
            return Response({
                "error": "Category does not exist"
            }, status=404)

    @swagger_auto_schema(tags=['Finance'],
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['income_id'],
                             properties={
                                 'income_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                             },
                         ),
                         )
    def delete(self, request, **kwargs):
        user = init_user(request)
        try:
            Income.objects.get(id=request.data.get("income_id"), user=user).delete()
        except Income.DoesNotExist:
            pass
        return Response(status=201)
