from django.shortcuts import redirect
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
@csrf_exempt
def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        "backend/Client_Secrets.json",
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['google_auth_state'] = state
    return redirect(authorization_url)


@api_view(['GET'])
@csrf_exempt
def GoogleCalendarRedirectView(request):
    code = request.query_params.get('code')
    if not code:
        return Response({'error': 'Missing authorization code'}, status=400)

    state = request.session.get('google_auth_state')
    flow = Flow.from_client_secrets_file(
        "backend/Client_Secrets.json",
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
        state=state
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10).execute()
    events = events_result.get('items', [])

    return Response({'events': events})
