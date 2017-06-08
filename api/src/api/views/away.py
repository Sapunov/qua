from django.shortcuts import redirect
from django.views.generic.base import View

from api.tracker import trackable


class AwayView(View):

    @trackable
    def get(self, request):

        params = request.GET

        redirect_url = params.get('redirect_url', '/')

        return redirect(redirect_url)
