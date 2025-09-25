import uuid
from rest_framework import serializers

from .models import Tender, Lot, Agrement, Qualif, Type, Domain, Category, Client, Meeting, RelAgrementLot, RelDomainTender, RelQualifLot

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label', 'rank', 'description']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'short', 'name', 'ministery', 'description']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'short', 'name', 'description']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'short', 'name', 'description']

class AgrementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agrement
        fields = ['id', 'short', 'name', 'description']

class QualifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualif
        fields = ['id', 'short', 'name', 'domain', 'classe', 'description']

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ['id', 'when', 'description', 'lot']

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'when', 'description', 'lot']

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'when', 'description', 'lot']

class LotSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    agrements = AgrementSerializer(many=True, read_only=True)
    qualifs = QualifSerializer(many=True, read_only=True)
    samples = SampleSerializer(many=True, read_only=True)
    meetings = MeetingSerializer(many=True, read_only=True)
    visits = VisitSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lot
        fields = [
            'id', 'number', 'title', 'description', 'estimate', 'bond', 
            'plans_price', 'reserved', 'variant', 'category', 'tender',
            'agrements', 'qualifs', 'samples', 'meetings', 'visits'
        ]

class TenderSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    type = TypeSerializer(read_only=True)
    domains = DomainSerializer(many=True, read_only=True)
    lots = LotSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tender
        fields = [
            'id', 'chrono', 'title', 'reference', 'published', 'deadline',
            'lots_count', 'estimate', 'bond', 'plans_price', 'reserved',
            'variant', 'category', 'location', 'ebid', 'esign', 'size_read',
            'size_bytes', 'address_withdrawal', 'address_bidding', 
            'address_opening', 'contact_name', 'contact_phone', 'contact_email',
            'contact_fax', 'created', 'updated', 'cancelled', 'link', 'acronym',
            'mode', 'procedure', 'client', 'type', 'domains', 'lots'
        ]

class RelAgrementLotSerializer(serializers.ModelSerializer):
    agrement = AgrementSerializer(read_only=True)
    lot = LotSerializer(read_only=True)
    
    class Meta:
        model = RelAgrementLot
        fields = ['agrement', 'lot']

class RelDomainTenderSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)
    tender = TenderSerializer(read_only=True)
    
    class Meta:
        model = RelDomainTender
        fields = ['domain', 'tender']

class RelQualifLotSerializer(serializers.ModelSerializer):
    qualif = QualifSerializer(read_only=True)
    lot = LotSerializer(read_only=True)
    
    class Meta:
        model = RelQualifLot
        fields = ['qualif', 'lot']