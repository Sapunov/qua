from django.shortcuts import redirect


def away_view(request):
    params = request.query_params

    redirect_url = params.get('redirect_url', '/')

    return redirect(redirect_url)
