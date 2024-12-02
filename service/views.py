from django.db.models import Sum
from django.utils.timezone import now, timedelta
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle, Component, ServiceIssue
# Vehicle Views
@csrf_exempt
def create_vehicle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vehicle = Vehicle.objects.create(
                make=data['make'],
                model=data['model'],
                year=data['year'],
                license_plate=data['license_plate'],
                owner_name=data['owner_name'],
                owner_contact=data['owner_contact']
            )
            return JsonResponse({'message': 'Vehicle created successfully!', 'vehicle_id': vehicle.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def get_vehicles(request):
    if request.method == 'GET':
        vehicles = list(Vehicle.objects.values())
        return JsonResponse(vehicles, safe=False)

# Component Views
@csrf_exempt
def create_component(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            component = Component.objects.create(
                name=data['name'],
                repair_price=data['repair_price'],
                new_price=data['new_price'],
                stock=data['stock']
            )
            return JsonResponse({'message': 'Component created successfully!', 'component_id': component.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def get_components(request):
    if request.method == 'GET':
        components = list(Component.objects.values())
        return JsonResponse(components, safe=False)

# Service Issue Views
@csrf_exempt
def create_service_issue(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vehicle = Vehicle.objects.get(id=data['vehicle_id'])
            component = Component.objects.get(id=data['component_id']) if 'component_id' in data else None
            service_issue = ServiceIssue.objects.create(
                vehicle=vehicle,
                component=component,
                is_repair=data['is_repair'],
                description=data['description'],
                cost=data['cost']
            )
            return JsonResponse({'message': 'Service issue created successfully!', 'service_issue_id': service_issue.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def get_service_issues(request):
    if request.method == 'GET':
        service_issues = list(ServiceIssue.objects.values())
        return JsonResponse(service_issues, safe=False)

def analytics_data(request):
    today = now().date()

    # Daily Revenue (Last 7 Days)
    daily_revenue = [
        {
            "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
            "revenue": ServiceIssue.objects.filter(
                created_at__date=(today - timedelta(days=i))
            ).aggregate(Sum('cost'))['cost__sum'] or 0,
        }
        for i in range(7)
    ]

    # Monthly Revenue (Last 12 Months)
    monthly_revenue = [
        {
            "month": (today - timedelta(days=30*i)).strftime("%B %Y"),
            "revenue": ServiceIssue.objects.filter(
                created_at__month=(today - timedelta(days=30*i)).month,
                created_at__year=(today - timedelta(days=30*i)).year,
            ).aggregate(Sum('cost'))['cost__sum'] or 0,
        }
        for i in range(12)
    ]

    # Yearly Revenue (Last 3 Years)
    yearly_revenue = [
        {
            "year": (today - timedelta(days=365*i)).year,
            "revenue": ServiceIssue.objects.filter(
                created_at__year=(today - timedelta(days=365*i)).year
            ).aggregate(Sum('cost'))['cost__sum'] or 0,
        }
        for i in range(3)
    ]

    # Combine all data
    data = {
        "daily_revenue": daily_revenue[::-1],  # Reverse for chronological order
        "monthly_revenue": monthly_revenue[::-1],
        "yearly_revenue": yearly_revenue[::-1],
    }
    return JsonResponse(data)