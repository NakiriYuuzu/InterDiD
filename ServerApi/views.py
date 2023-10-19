from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ServerApi.serializer import *
from ServerCommon.models import *


class BeaconsView(APIView):
    @staticmethod
    def get(request):
        user = request.user
        if not user.is_authenticated:  # 驗證用戶是否已經登錄
            return Response({'error': 'Authentication is required'}, status=status.HTTP_401_UNAUTHORIZED)

        beacon_id = request.query_params.get('beacon_id', None)
        if beacon_id:
            beacons = Beacons.objects.filter(beacon_id=beacon_id)
        else:
            beacons = Beacons.objects.all()
        serializer = BeaconsSerializer(beacons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request):
        user = request.user
        if not user.is_authenticated:  # 驗證用戶是否已經登錄
            return Response({'error': 'Authentication is required'}, status=status.HTTP_401_UNAUTHORIZED)

        beacon_id = request.data.get('beacon_id')  # 從請求數據中獲取 beacon_id
        if beacon_id is None:
            return Response({'error': 'Beacon ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            beacon = Beacons.objects.get(beacon_id=beacon_id)
        except Beacons.DoesNotExist:
            return Response({'error': 'Beacon not found'}, status=status.HTTP_404_NOT_FOUND)

        beacon.delete()
        return Response({'message': 'Beacon deleted successfully'}, status=status.HTTP_200_OK)
