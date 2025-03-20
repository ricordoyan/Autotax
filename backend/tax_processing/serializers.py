from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Dependent, TaxDocument, TaxReturn

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class DependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependent
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    dependents = DependentSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class TaxDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDocument
        fields = '__all__'
        read_only_fields = ('user', 'status', 'extracted_data')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TaxReturnSerializer(serializers.ModelSerializer):
    documents = TaxDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = TaxReturn
        fields = '__all__'
        read_only_fields = ('user', 'status', 'total_income', 'total_deductions',
                          'total_tax', 'refund_amount', 'filed_date', 'tax_data')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 