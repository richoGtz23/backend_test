from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend_test.constants.payload import OK, NOT_OK
from backend_test.models.numToEnglish import NumToEnglish
from backend_test.models.payload import Payload as Payload
from backend_test.serializers.payload import PayloadSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated, ))
@csrf_protect
def num_to_english_view(request):
    number = None
    if request.method == 'GET':
        number = request.query_params.get('number')
    elif request.method == 'POST':
        number = request.data.get('number')
    num_to_english_proccessor = NumToEnglish(number)
    msg_status, text = num_to_english_proccessor.process()
    payload = Payload(status=msg_status, num_in_english=text)
    response_status = status.HTTP_200_OK
    if msg_status in NOT_OK:
        response_status = status.HTTP_400_BAD_REQUEST
    return Response(PayloadSerializer(payload).data, status=response_status)
