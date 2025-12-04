from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .services import process_user_query

class ChatbotQueryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"detail": "Falta el campo 'query'."}, status=400)

        result = process_user_query(query)
        return Response(result, status=status.HTTP_200_OK)
