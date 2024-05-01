import os
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()
    total_completed_pos = completed_pos.count()
    
    if total_completed_pos == 0:
        return 0.0
    return (on_time_deliveries / total_completed_pos) * 100

def calculate_quality_rating_avg(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating=None)
    
    if completed_pos.count() == 0:
        return 0.0
    
    total_rating = completed_pos.aggregate(Sum('quality_rating'))['quality_rating__sum']
    return total_rating / completed_pos.count()

def calculate_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    
    if acknowledged_pos.count() == 0:
        return 0.0
    
    total_response_time = sum(
        (po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos
    )
    
    return total_response_time / acknowledged_pos.count()

def calculate_fulfillment_rate(vendor):
    pos = PurchaseOrder.objects.filter(vendor=vendor)
    completed_pos = pos.filter(status='completed')
    successful_pos = completed_pos.filter(status='successful')
    
    if pos.count() == 0:
        return 0.0
    
    return (successful_pos.count() / pos.count()) * 100

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_avg(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfillment_rate = calculate_fulfillment_rate(vendor)
        
        performance_data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        
        return Response(performance_data)

class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, pk=po_id)
        po.acknowledgment_date = timezone.now()
        po.save()
        
        return Response({'message': 'Purchase Order acknowledged'}, status=status.HTTP_200_OK)

def dbDownload(request):
    if request.user.is_superuser:
        os.system("cp db.sqlite3 static/")
        return HttpResponse("<a href='/static/db.sqlite3' download>Download</a>")