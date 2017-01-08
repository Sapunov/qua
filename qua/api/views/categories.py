from rest_framework import views, status
from django.http import Http404

from qua.api.response import QuaApiResponse
from qua.api.models import Categories
from qua.api import serializers


class CategoriesBase(views.APIView):
    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            raise Http404


class CategoriesListView(CategoriesBase):
    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = serializers.CategoriesListSerializer(categories, many=True)

        return QuaApiResponse(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.CategoriesDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

            return QuaApiResponse(serializer.data, status=status.HTTP_201_CREATED)


class CategoriesDetailView(CategoriesBase):
    def get(self, request, category_id, format=None):
        category = self.get_object(category_id)
        serializer = serializers.CategoriesListSerializer(category)

        return QuaApiResponse(serializer.data)

    def put(self, request, category_id, format=None):
        category = self.get_object(category_id)
        serializer = serializers.CategoriesDetailSerializer(
            category, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

            return QuaApiResponse(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, category_id, format=None):
        category = self.get_object(category_id)
        category.delete()

        return QuaApiResponse(status=status.HTTP_204_NO_CONTENT)
