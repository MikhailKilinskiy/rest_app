from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

from .serializers import CostSerializer
from .models import Cost
from .permissions import IsAutentificated

class CostService(APIView):
    permission_classes = (IsAutentificated,)
    serializer_class = CostSerializer

    def _get_object(self, pk):
        try:
            return Cost.objects.get(pk=pk)
        except:
            return Response({"status": "Object not found"}, status.HTTP_404_NOT_FOUND)

    def _create_data_from_request(self, request):
        try:
            payload = request.data
        except:
            payload = request.data.dict()
        user = request.user.id
        payload["user"] = user
        return payload

    def get(self, request):
        costs = Cost.objects.all()
        serializer = self.serializer_class(costs, many=True)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    def post(self, request):
        payload = self._create_data_from_request(request)
        try:
            serializer = self.serializer_class(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            content = {"status": "INTERNAL SERVER ERROR", "error": str(ex)}
            return Response(content, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        payload = self._create_data_from_request(request)
        cost = self._get_object(payload['id'])
        try:
            if(request.user == cost.user):
                serializer = self.serializer_class(cost, data=payload)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": "UNAUTHORIZED"}, status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            content = {"status": "INTERNAL SERVER ERROR", "error": str(ex)}
            return Response(content, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        payload = self._create_data_from_request(request)
        cost = self._get_object(payload['id'])
        try:
            if (request.user == cost.user):
                cost.delete()
                content = {"status": "NO CONTENT"}
                return Response(content, status.HTTP_204_NO_CONTENT)
            else:
                return Response({"status": "UNAUTHORIZED"}, status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            content = {"status": "INTERNAL SERVER ERROR", "error": str(ex)}
            return Response(content, status.HTTP_500_INTERNAL_SERVER_ERROR)
