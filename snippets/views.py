from rest_framework import generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer,UserSerializer
from rest_framework import permissions
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from rest_framework import renderers
from rest_framework.response import Response

# Create your views here.


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_class = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format)
    })




class SnippetList(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer



class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
