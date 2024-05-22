import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from app_main.models import Note
from .serializers import NoteSerializer, UserSerializer

User = get_user_model()

@api_view(['GET'])
def get_notes(request):
    notes = Note.objects.all()
    serialized_data = NoteSerializer(instance=notes, many=True)
    return Response(data=serialized_data.data)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serialized_data = UserSerializer(instance=users, many=True)
    return Response(data=serialized_data.data)

@api_view(['POST'])
def create_note(request):
    if request.method == 'POST':
        owner_id = request.data.get('owner')
        title = request.data.get('title')
        body = request.data.get('body')

        errors = []

        if not owner_id:
            errors.append({"owner": "Note should have an owner"})

        if not title:
            errors.append({"title": "Note should have a title"})

        if errors:
            return Response(data=json.dumps(errors), status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=owner_id)
        note = Note.objects.create(owner=user, title=title, body=body)
        note.save()
        return Response(data="Created", status=status.HTTP_201_CREATED)

    return Response()

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        errors = []

        if not username:
            errors.append({"username": "Username is required"})

        if not password:
            errors.append({"password": "Password is required"})

        if not email:
            errors.append({"email": "Email is required"})

        if errors:
            return Response(data=json.dumps(errors), status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return Response(data={"username": user.username, "email": user.email}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PATCH', 'DELETE'])
def note_detail(request, id):
    try:
        note = Note.objects.get(id=id)
    except Note.DoesNotExist:
        return Response(data={'detail': 'No such note with this ID'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        note = NoteSerializer(instance=note, many=False).data
        return Response(data=note)

    elif request.method == 'PATCH':
        title = request.data.get('title')
        body = request.data.get('body')

        if title:
            note.title = title

        if body:
            note.body = body

        note.save()
        note = NoteSerializer(instance=note, many=False).data
        return Response(data=note)

    elif request.method == 'DELETE':
        note.delete()
        return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PATCH', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(data={'detail': 'No such user with this ID'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_data = UserSerializer(instance=user, many=False).data
        return Response(data=user_data)

    elif request.method == 'PATCH':
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        if username:
            user.username = username

        if email:
            user.email = email

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if password:
            user.set_password(password)

        user.save()
        user_data = UserSerializer(instance=user, many=False).data
        return Response(data=user_data)

    elif request.method == 'DELETE':
        user.delete()
        return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
