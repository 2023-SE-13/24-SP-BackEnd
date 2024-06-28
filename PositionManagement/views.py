import json

import pytz
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from CompanyManagement.models import CompanyMember
from PositionManagement.models import Position, Application
from PositionManagement.serializer import PositionSerializer
from UserManagement.models import User
from shared.decorators import require_position, require_company


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_position(request):
    data = json.loads(request.body.decode('utf-8'))
    cur_user = request.user
    cm = CompanyMember.objects.filter(user=cur_user).first()
    if cm is None:
        return JsonResponse({"status": "error", "message": "You are not a member of any company"},
                            status=status.HTTP_400_BAD_REQUEST)
    if cm.role == 'Staff':
        return JsonResponse({"status": "error", "message": "You are not allowed to create position"},
                            status=status.HTTP_400_BAD_REQUEST)
    company = cm.company
    position_name = data.get('position_name')
    position_description = data.get('position_description')
    location = data.get('location')
    education_requirement = data.get('education_requirement')
    salary_min = data.get('salary_min')
    salary_max = data.get('salary_max')
    if not position_name or not position_description:
        return JsonResponse(
            {"status": "error", "message": "position_name, position_description are required"},
            status=status.HTTP_406_NOT_ACCEPTABLE)
    position = Position(company=company, position_name=position_name, position_description=position_description,
                        location=location, education_requirement=education_requirement, salary_min=salary_min, salary_max=salary_max)
    position.save()
    return JsonResponse({'status': 'success'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['GET'])
@require_position
def get_position(request):
    position = request.position_object
    serializer = PositionSerializer(position)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_position
def delete_position(request):
    position = request.position_object
    cur_user = request.user
    cm = CompanyMember.objects.filter(user=cur_user).first()
    if cm is None:
        return JsonResponse({"status": "error", "message": "You are not a member of any company"},
                            status=status.HTTP_400_BAD_REQUEST)
    if cm.role == 'Staff':
        return JsonResponse({"status": "error", "message": "You are not allowed to delete position"},
                            status=status.HTTP_400_BAD_REQUEST)
    position.delete()
    return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@require_company
def get_position_list(request):
    company = request.company_object
    positions = Position.objects.filter(company=company)
    serializer = PositionSerializer(positions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_position
def apply_position(request):
    cur_usr = request.user
    position = request.position_object
    if Application.objects.filter(user=cur_usr, position=position).exists():
        return JsonResponse({"status": "error", "message": "You have already applied for this position"},
                            status=status.HTTP_400_BAD_REQUEST)
    if cur_usr.is_staff:
        return JsonResponse({"status": "error", "message": "Staff cannot apply for position"},
                            status=status.HTTP_400_BAD_REQUEST)
    if User.objects.get(username=cur_usr.username).resume is None:
        return JsonResponse({"status": "error", "message": "Please upload your resume before applying for a position"},
                            status=status.HTTP_400_BAD_REQUEST)
    tz = pytz.timezone('Asia/Shanghai')
    utc8time = timezone.now().astimezone(tz)
    application = Application(user=cur_usr, position=position, applied_at=utc8time)
    application.save()
    return JsonResponse({'status': 'success'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@require_position
def get_position_applications(request):
    cur_user = request.user
    position = request.position_object
    company = position.company
    cm = CompanyMember.objects.filter(user=cur_user, company=company).first()
    if cm is None or cm.role == 'Staff':
        return JsonResponse({"status": "error", "message": "You are not allowed to view applications"},
                            status=status.HTTP_400_BAD_REQUEST)
    applications = Application.objects.filter(position__position_id=position.position_id)
    result = []
    for application in applications:
        result.append({
            'username': application.user.username,
            'real_name': application.user.real_name,
            'education': application.user.education,
            'desired_position': application.user.desired_position,
            'skills': [skill.name for skill in application.user.skills.all()],
            'applied_at': application.applied_at,
        })
    return JsonResponse(result, status=status.HTTP_200_OK, safe=False)
