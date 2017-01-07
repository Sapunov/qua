from rest_framework import views, status
from rest_framework.response import Response
from django.http import Http404

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

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.CategoriesDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesDetailView(CategoriesBase):
    def get(self, request, category_id, format=None):
        category = self.get_object(category_id)
        serializer = serializers.CategoriesListSerializer(category)

        return Response(serializer.data)

    def put(self, request, category_id, format=None):
        category = self.get_object(category_id)
        serializer = serializers.CategoriesDetailSerializer(
            category, data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id, format=None):
        category = self.get_object(category_id)
        category.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
