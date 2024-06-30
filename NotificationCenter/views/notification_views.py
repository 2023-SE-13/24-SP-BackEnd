import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from NotificationCenter.models import Notification
from NotificationCenter.serializers import NotificationSerializer
from NotificationCenter.views.utils.notifications import create_notification
from shared.decorators import require_user


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_notification(request):
    notification_id = request.GET.get('notification_id')
    notification = Notification.objects.get(notification_id=notification_id)
    if notification.notification_type == 'group_chat':
        message = notification.message
        group_id = notification.message.group.group_id
        message_id = notification.message.message_id
        notification_data = {
            "notification_id": notification.notification_id,
            "notification_type": "group_chat",
            "message_id": message_id,
            "group_id": group_id,
            "created_at": notification.created_at,
            "content": notification.content,
        }
    elif notification.notification_type == 'document':
        doc = notification.doc
        doc_id = doc.doc_id
        notification_data = {
            "notification_id": notification.notification_id,
            "notification_type": "document",
            "doc_id": doc_id,
            "project_id": doc.project.project_id,
            "team_id": doc.project.team.team_id,
            "created_at": notification.created_at,
            "content": notification.content,
        }
    else:
        notification_data = {
            "notification_id": notification.notification_id,
            "notification_type": "system",
            "created_at": notification.created_at,
            "content": notification.content,
        }
    return Response({"status": "success", "data": notification_data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_notifications(request):
    user = request.user
    require_type = request.GET.get('require_type')
    notifications = None
    if require_type == 'ALL':
        notifications = Notification.objects.filter(user=user)

    elif require_type == '@':
        notifications = Notification.objects. \
            filter(Q(user=user) & (Q(notification_type='group_chat') | Q(notification_type='document')))

    elif require_type == 'system':
        notifications = Notification.objects.filter(user=user, notification_type='system')

    serializer = NotificationSerializer(notifications, many=True)
    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_notification(request):
    notification_id = request.GET.get('notification_id')
    is_read = request.GET.get('is_read')
    notification = Notification.objects.get(notification_id=notification_id)
    notification.is_read = is_read
    notification.save()
    return Response({"status": "success"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_notification(request):
    notification_id = request.GET.get('notification_id')
    notification = Notification.objects.get(notification_id=notification_id)
    notification.delete()
    return Response({"status": "success"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_read_notifications(request):
    user = request.user
    Notification.objects.filter(user=user, is_read=True).delete()
    return Response({"status": "success"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def read_all_notifications(request):
    user = request.user
    Notification.objects.filter(user=user).update(is_read=True)
    return Response({"status": "success"}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_user
def create_doc_notification(request):
    current_user = request.user
    user_to_notice = request.user_object
    doc_id = request.data.get('doc_id', None)
    json_str = json.dumps({
        "username": user_to_notice.username,
        "notification_type": "document",
        "doc_id": doc_id,
        "content": f"{current_user.username} shared a document with you",
    })
    notification = create_notification(json_str)
    return JsonResponse({"status": "success", "message": "Notification created successfully"},
                        status=status.HTTP_200_OK)