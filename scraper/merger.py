from rest_framework import serializers
from django.db import transaction
from .models import (Tender, Lot, Meeting, Domain, Category, Client, 
    Type, Agrement, Qualif, RelDomainTender, RelAgrementLot, RelQualifLot
)
from .serializers import (
    TenderSerializer, LotSerializer, MeetingSerializer, DomainSerializer,
    CategorySerializer, ClientSerializer, TypeSerializer, AgrementSerializer,
    QualifSerializer, RelDomainTenderSerializer, RelAgrementLotSerializer, RelQualifLotSerializer
)

@transaction.atomic
def mergeTender(json_data):
    """
    Merge a nested JSON object into a Tender instance and its related objects in the database.
    Assumes no 'id' fields in the JSON. Deletes related objects (Lots, Meetings, etc.) that are
    absent in the JSON but present in the database.

    Args:
        json_data (dict): Nested JSON object representing a Tender instance without IDs.

    Returns:
        Tender: The created or updated Tender instance.

    Raises:
        serializers.ValidationError: If the JSON data is invalid.
    """
    # Step 1: Validate the JSON using TenderSerializer
    tender_serializer = TenderSerializer(data=json_data)
    tender_serializer.is_valid(raise_exception=True)
    validated_data = tender_serializer.validated_data

    # Step 2: Handle foreign key relationships (category, client, type)
    category_data = validated_data.pop('category', None)
    client_data = validated_data.pop('client', None)
    type_data = validated_data.pop('type', None)

    # Handle Category
    category = None
    if category_data:
        label = category_data.get('label')
        if label and Category.objects.filter(label=label).exists():
            category = Category.objects.get(label=label)
            category_serializer = CategorySerializer(category, data=category_data, partial=True)
        else:
            category_serializer = CategorySerializer(data=category_data)
        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()

    # Handle Client
    client = None
    if client_data:
        short = client_data.get('short')
        name = client_data.get('name')
        if short and Client.objects.filter(short=short).exists():
            client = Client.objects.get(short=short)
            client_serializer = ClientSerializer(client, data=client_data, partial=True)
        elif name and Client.objects.filter(name=name).exists():
            client = Client.objects.get(name=name)
            client_serializer = ClientSerializer(client, data=client_data, partial=True)
        else:
            client_serializer = ClientSerializer(data=client_data)
        client_serializer.is_valid(raise_exception=True)
        client = client_serializer.save()

    # Handle Type
    type_obj = None
    if type_data:
        short = type_data.get('short')
        name = type_data.get('name')
        if short and Type.objects.filter(short=short).exists():
            type_obj = Type.objects.get(short=short)
            type_serializer = TypeSerializer(type_obj, data=type_data, partial=True)
        elif name and Type.objects.filter(name=name).exists():
            type_obj = Type.objects.get(name=name)
            type_serializer = TypeSerializer(type_obj, data=type_data, partial=True)
        else:
            type_serializer = TypeSerializer(data=type_data)
        type_serializer.is_valid(raise_exception=True)
        type_obj = type_serializer.save()

    # Step 3: Create or update Tender
    reference = validated_data.get('reference')
    title = validated_data.get('title')
    chrono = validated_data.get('chrono')
    tender = None
    if chrono and Tender.objects.filter(chrono=chrono).exists():
        tender = Tender.objects.get(chrono=chrono)
        tender_serializer = TenderSerializer(tender, data=validated_data, partial=True)
    # elif title and chrono and Tender.objects.filter(title=title, chrono=chrono).exists():
    #     tender = Tender.objects.get(title=title, chrono=chrono)
    #     tender_serializer = TenderSerializer(tender, data=validated_data, partial=True)
    else:
        tender_serializer = TenderSerializer(data=validated_data)
    tender_serializer.is_valid(raise_exception=True)
    tender = tender_serializer.save(category=category, client=client, type=type_obj)

    # Step 4: Handle Domains (many-to-many)
    domains_data = validated_data.pop('domains', [])
    json_domain_keys = set()
    for domain_data in domains_data:
        # short = domain_data.get('short')
        name = domain_data.get('name')
        domain = None
        if name and Domain.objects.filter(name=name).exists():
            domain = Domain.objects.get(name=name)
            domain_serializer = DomainSerializer(domain, data=domain_data, partial=True)
        # elif short and Domain.objects.filter(short=short).exists():
        #     domain = Domain.objects.get(short=short)
        #     domain_serializer = DomainSerializer(domain, data=domain_data, partial=True)
        else:
            domain_serializer = DomainSerializer(data=domain_data)
        domain_serializer.is_valid(raise_exception=True)
        domain = domain_serializer.save()
        json_domain_keys.add((domain.name))
        RelDomainTender.objects.get_or_create(domain=domain, tender=tender)

    # Remove domains not in JSON
    existing_domains = set(tender.domains.values_list('name'))
    domains_to_remove = existing_domains - json_domain_keys
    for short, name in domains_to_remove:
        domain = Domain.objects.filter(name=name).first()
        if domain:
            RelDomainTender.objects.filter(domain=domain, tender=tender).delete()

    # Step 5: Handle Lots
    lots_data = validated_data.pop('lots', [])
    json_lot_keys = set()
    new_lots = []

    for lot_data in lots_data:
        # Handle nested Category for Lot
        lot_category_data = lot_data.pop('category', None)
        lot_category = None
        if lot_category_data:
            label = lot_category_data.get('label')
            if label and Category.objects.filter(label=label).exists():
                lot_category = Category.objects.get(label=label)
                lot_category_serializer = CategorySerializer(lot_category, data=lot_category_data, partial=True)
            else:
                lot_category_serializer = CategorySerializer(data=lot_category_data)
            lot_category_serializer.is_valid(raise_exception=True)
            lot_category = lot_category_serializer.save()

        # Handle nested Meetings, Agrements, Qualifs
        meetings_data = lot_data.pop('meetings', [])
        agrements_data = lot_data.pop('agrements', [])
        qualifs_data = lot_data.pop('qualifs', [])
        lot_data['category'] = lot_category

        # Match Lot by title or number
        lot_title = lot_data.get('title')
        lot_number = lot_data.get('number')
        lot = None
        if lot_title and Lot.objects.filter(title=lot_title, tender=tender).exists():
            lot = Lot.objects.get(title=lot_title, tender=tender)
            lot_serializer = LotSerializer(lot, data=lot_data, partial=True)
        elif lot_number is not None and Lot.objects.filter(number=lot_number, tender=tender).exists():
            lot = Lot.objects.get(number=lot_number, tender=tender)
            lot_serializer = LotSerializer(lot, data=lot_data, partial=True)
        else:
            lot_serializer = LotSerializer(data=lot_data)
        lot_serializer.is_valid(raise_exception=True)
        lot = lot_serializer.save(tender=tender)

        json_lot_keys.add((lot.title, lot.number))

        # Handle Meetings
        json_meeting_keys = set()
        for meeting_data in meetings_data:
            when = meeting_data.get('when')
            description = meeting_data.get('description')
            json_meeting_keys.add((when, description))
            meeting = None
            if when and Meeting.objects.filter(when=when, lot=lot).exists():
                meeting = Meeting.objects.get(when=when, lot=lot)
                meeting_serializer = MeetingSerializer(meeting, data=meeting_data, partial=True)
            else:
                meeting_serializer = MeetingSerializer(data=meeting_data)
            meeting_serializer.is_valid(raise_exception=True)
            meeting_serializer.save(lot=lot)

        # Remove Meetings not in JSON
        existing_meetings = set(lot.meetings.values_list('when', 'description'))
        meetings_to_remove = existing_meetings - json_meeting_keys
        for when, description in meetings_to_remove:
            Meeting.objects.filter(when=when, description=description, lot=lot).delete()

        # Handle Agrements (many-to-many)
        json_agrement_keys = set()
        for agrement_data in agrements_data:
            short = agrement_data.get('short')
            name = agrement_data.get('name')
            agrement = None
            if short and Agrement.objects.filter(short=short).exists():
                agrement = Agrement.objects.get(short=short)
                agrement_serializer = AgrementSerializer(agrement, data=agrement_data, partial=True)
            elif name and Agrement.objects.filter(name=name).exists():
                agrement = Agrement.objects.get(name=name)
                agrement_serializer = AgrementSerializer(agrement, data=agrement_data, partial=True)
            else:
                agrement_serializer = AgrementSerializer(data=agrement_data)
            agrement_serializer.is_valid(raise_exception=True)
            agrement = agrement_serializer.save()
            json_agrement_keys.add((agrement.short, agrement.name))
            RelAgrementLot.objects.get_or_create(agrement=agrement, lot=lot)

        # Remove Agrements not in JSON
        existing_agrements = set(lot.agrements.values_list('short', 'name'))
        agrements_to_remove = existing_agrements - json_agrement_keys
        for short, name in agrements_to_remove:
            agrement = Agrement.objects.filter(short=short, name=name).first()
            if agrement:
                RelAgrementLot.objects.filter(agrement=agrement, lot=lot).delete()

        # Handle Qualifs (many-to-many)
        json_qualif_keys = set()
        for qualif_data in qualifs_data:
            short = qualif_data.get('short')
            name = qualif_data.get('name')
            qualif = None
            if short and Qualif.objects.filter(short=short).exists():
                qualif = Qualif.objects.get(short=short)
                qualif_serializer = QualifSerializer(qualif, data=qualif_data, partial=True)
            elif name and Qualif.objects.filter(name=name).exists():
                qualif = Qualif.objects.get(name=name)
                qualif_serializer = QualifSerializer(qualif, data=qualif_data, partial=True)
            else:
                qualif_serializer = QualifSerializer(data=qualif_data)
            qualif_serializer.is_valid(raise_exception=True)
            qualif = qualif_serializer.save()
            json_qualif_keys.add((qualif.short, qualif.name))
            RelQualifLot.objects.get_or_create(qualif=qualif, lot=lot)

        # Remove Qualifs not in JSON
        existing_qualifs = set(lot.qualifs.values_list('short', 'name'))
        qualifs_to_remove = existing_qualifs - json_qualif_keys
        for short, name in qualifs_to_remove:
            qualif = Qualif.objects.filter(short=short, name=name).first()
            if qualif:
                RelQualifLot.objects.filter(qualif=qualif, lot=lot).delete()

        new_lots.append(lot)

    # Remove Lots not in JSON
    existing_lots = set(tender.lots.values_list('title', 'number'))
    lots_to_remove = existing_lots - json_lot_keys
    for title, number in lots_to_remove:
        Lot.objects.filter(title=title, number=number, tender=tender).delete()

    return tender