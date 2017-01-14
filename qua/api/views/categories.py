from rest_framework.views import APIView

from qua.api.models import Category
from qua.api.response import QuaApiResponse
from qua.api.serializers import CategorySerializer, CategoryListSerializer
from qua.api.serializers import serialize, deserialize
from qua.api.utils.shortcuts import get_object


class CategoryListView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = serialize(CategoryListSerializer, categories, many=True)

        return QuaApiResponse(serializer.data)

    def post(self, request, format=None):
        serializer = deserialize(CategorySerializer, data=request.data)
        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)


class CategoryView(APIView):

    def get(self, request, category_id, format=None):
        category = get_object(Category, category_id)
        serializer = serialize(CategoryListSerializer, category)

        return QuaApiResponse(serializer.data)

    def put(self, request, category_id, format=None):
        category = get_object(Category, category_id)
        serializer = serialize(CategorySerializer, category, data=request.data)

        serializer.save(user=request.user)

        return QuaApiResponse(serializer.data)

    def delete(self, request, category_id, format=None):
        category = get_object(Category, category_id)
        category.delete()

        return QuaApiResponse()
