from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import UserProfile, Dependent, TaxDocument, TaxReturn
from .serializers import (
    UserProfileSerializer,
    DependentSerializer,
    TaxDocumentSerializer,
    TaxReturnSerializer,
)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]  # Temporarily allow all access for testing

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.none()

class DependentViewSet(viewsets.ModelViewSet):
    serializer_class = DependentSerializer
    permission_classes = [AllowAny]  # Temporarily allow all access for testing

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Dependent.objects.filter(user_profile__user=self.request.user)
        return Dependent.objects.none()

class TaxDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = TaxDocumentSerializer
    permission_classes = [AllowAny]  # Temporarily allow all access for testing

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TaxDocument.objects.filter(user=self.request.user)
        return TaxDocument.objects.none()

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        document = self.get_object()
        document.status = 'PROCESSING'
        document.save()

        try:
            # Here we would integrate with AI/ML services for document processing
            # For demo purposes, we'll just update with dummy data
            document.extracted_data = {
                'employer': 'Example Corp',
                'wages': 50000,
                'tax_withheld': 10000,
            }
            document.status = 'PROCESSED'
            document.save()
            return Response({'status': 'success'})
        except Exception as e:
            document.status = 'ERROR'
            document.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TaxReturnViewSet(viewsets.ModelViewSet):
    serializer_class = TaxReturnSerializer
    permission_classes = [AllowAny]  # Temporarily allow all access for testing

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TaxReturn.objects.filter(user=self.request.user)
        return TaxReturn.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # For demo purposes, create a default user if not authenticated
            from django.contrib.auth.models import User
            default_user, _ = User.objects.get_or_create(username='demo_user')
            serializer.save(user=default_user)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        tax_return = self.get_object()
        tax_return.status = 'IN_PROGRESS'
        tax_return.save()

        try:
            # Here we would integrate with AI services for tax return processing
            # For demo purposes, we'll calculate using dummy logic
            documents = tax_return.documents.all()
            total_income = sum(
                doc.extracted_data.get('wages', 0)
                for doc in documents
                if doc.status == 'PROCESSED'
            )
            total_tax = sum(
                doc.extracted_data.get('tax_withheld', 0)
                for doc in documents
                if doc.status == 'PROCESSED'
            )

            tax_return.total_income = total_income
            tax_return.total_tax = total_tax
            tax_return.refund_amount = total_tax * 0.1  # Dummy calculation
            tax_return.status = 'COMPLETED'
            tax_return.save()

            return Response(TaxReturnSerializer(tax_return).data)
        except Exception as e:
            tax_return.status = 'DRAFT'
            tax_return.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        tax_return = self.get_object()
        if tax_return.status != 'COMPLETED':
            return Response(
                {'error': 'Tax return must be completed before submission'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Here we would integrate with e-filing services
            # For demo purposes, we'll just mark it as filed
            tax_return.status = 'FILED'
            tax_return.save()
            return Response({'status': 'success'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 