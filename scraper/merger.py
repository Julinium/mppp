import traceback
from rest_framework import serializers
from django.db import transaction

import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")
django.setup()

from . import helper


from .models import (
    Tender, Lot, Agrement, Qualif, Kind, Domain, Mode, Procedure, 
    Category, Change, Client, Meeting, Sample, Visit,
    RelAgrementLot, RelDomainTender, RelQualifLot
)

from .serializers import (
    TenderSerializer, LotSerializer, MeetingSerializer, SampleSerializer, VisitSerializer, 
    ModeSerializer, ProcedureSerializer, DomainSerializer, 
    CategorySerializer, ChangeSerializer, ClientSerializer, KindSerializer, AgrementSerializer, 
    QualifSerializer, RelDomainTenderSerializer, RelAgrementLotSerializer, 
    RelQualifLotSerializer
)



def json2Data(tender_json):

    helper.printMessage('DEBUG', 'merger.json2Data', "### Started formatting tender data ...", 1, 0)
    j = tender_json
    try:
        j["published"] = helper.getDateTime(j["published"])
        j["deadline"] = helper.getDateTime(j["deadline"])
        j["cancelled"] = j["cancelled"] == "Oui"
        j["plans_price"] = helper.getAmount(j["plans_price"])
        j["acronym"] = j["link"].split("=")[1]

        ebs = j["ebid_esign"] # 1: Required, 0: Not required, Else: NA
        match ebs:  # Look at the image ...
            case "reponse-elec-oblig": # cons_repec = 'RO'
                j["ebid"] = 1
                j["esign"] = 0                
            case "reponse-elec": #cons_repec = 'OO'
                j["ebid"] = 0
                j["esign"] = 0
            case "reponse-elec-oblig-avec-signature": #cons_repec = 'RR'
                j["ebid"] = 1
                j["esign"] = 1
            case "reponse-elec-avec-signature": # cons_repec = 'OR'
                j["ebid"] = 0
                j["esign"] = 1
            # case "reponse-elec-non": # cons_repec = 'I'

        ll = j["lots"]
        for l in ll:
            l["estimate"] = helper.getAmount(l["estimate"])
            l["bond"] = helper.getAmount(l["bond"])
            l["variant"] = l["variant"] == "Oui"
            l["reserved"] = l["reserved"] == "Oui"
            ss = l["samples"]
            if len(ss) > 0:
                for s in ss:
                    s["when"] = helper.getDateTime(s["when"])
                l["samples"] = ss
            mm = l["meetings"]
            if len(mm) > 0:
                for m in mm:
                    m["when"] = helper.getDateTime(m["when"])
                l["meetings"] = mm
            vv = l["visits"]
            if len(vv) > 0:
                for v in vv:
                    v["when"] = helper.getDateTime(v["when"])
                l["visits"] = vv
        j["lots"] = ll
        helper.printMessage('DEBUG', 'merger.json2Data', "+++ Done formatting tender data")

    except:
        traceback.print_exc()

    return j


@transaction.atomic
def saveTender(tender_data):
    """
    # Merge a nested JSON object into a Tender instance and its related objects in the database.
    # Assumes no 'id' fields in the JSON. Deletes related objects (Lots, Meetings, etc.) that are
    # absent in the JSON but present in the database.

    # Args:
    #     tender_data (dict): Nested JSON object representing a Tender instance without IDs.

    # Returns:
    #     Tender: The created or updated Tender instance.

    # Raises:
    #     serializers.ValidationError: If the JSON data is invalid.
    """

    formatted_data = json2Data(tender_data)
    helper.printMessage('DEBUG', 'merger.saveTender', "### Started saving formatted date", 1, 0)

    # Step x: Validate the JSON using TenderSerializer
    tender_serializer = TenderSerializer(data=formatted_data)
    tender_serializer.is_valid(raise_exception=True)
    validated_data = tender_serializer.validated_data

    # Step x: Handle foreign key relationships (category, client, kind, mode, procedure)
    category_data = formatted_data['category']
    client_data = formatted_data['client']
    kind_data = formatted_data['kind']
    mode_data = formatted_data['mode']
    procedure_data = formatted_data['procedure']

    ## Handle Category
    category = None
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Category ... ")
    if category_data:
        helper.printMessage('TRACE', 'merger.saveTender', "+++ Got Category data. Analyzing ... ")
        label = category_data.get('label')
        if label and Category.objects.filter(label=label).exists():
            category = Category.objects.get(label=label)
            category_serializer = CategorySerializer(category, data=category_data, partial=True)
            helper.printMessage('DEBUG', 'merger.saveTender', "+++ Category already exists. Skipping.")
        else:
            category_serializer = CategorySerializer(data=category_data)
            helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Category to be created: {label}")
            category_serializer.is_valid(raise_exception=True)
            category = category_serializer.save()
    else:
        helper.printMessage('WARN', 'merger.saveTender', "--- Could not pop out Category data!", 1, 2)

    ## Handle Client
    client = None
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Client ... ")
    if client_data:
        name = client_data.get('name')
        if name and Client.objects.filter(name=name).exists():
            client = Client.objects.get(name=name)
            client_serializer = ClientSerializer(client, data=client_data, partial=True)
            helper.printMessage('DEBUG', 'merger.saveTender', "+++ Client already exists. Skipping.")
        else:
            client_serializer = ClientSerializer(data=client_data)
            helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Client to be created: {name}")
            client_serializer.is_valid(raise_exception=True)
            client = client_serializer.save()

    ## Handle Kind
    kind = None
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Type ... ")
    if kind_data:
        name = kind_data.get('name')
        if name and Kind.objects.filter(name=name).exists():
            kind = Kind.objects.get(name=name)
            kind_serializer = KindSerializer(kind, data=kind_data, partial=True)
            helper.printMessage('DEBUG', 'merger.saveTender', "+++ Procedure Type already exists. Skipping.")
        else:
            kind_serializer = KindSerializer(data=kind_data)
            helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Procedure Type to be created: {name}")
            kind_serializer.is_valid(raise_exception=True)
            kind = kind_serializer.save()

    ## Handle Mode
    mode = None
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Mode ... ")
    if mode_data:
        name = mode_data.get('name')
        if name and Mode.objects.filter(name=name).exists():
            mode = Mode.objects.get(name=name)
            mode_serializer = ModeSerializer(mode, data=mode_data, partial=True)
            helper.printMessage('DEBUG', 'merger.saveTender', "+++ Awarding Mode already exists. Skipping.")
        else:
            mode_serializer = ModeSerializer(data=mode_data)
            helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Awarding Mode to be created: {name}")
            mode_serializer.is_valid(raise_exception=True)
            mode = mode_serializer.save()

    ## Handle Procedure
    procedure = None
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Procedure ... ")
    if procedure_data:
        name = procedure_data.get('name')
        if name and Procedure.objects.filter(name=name).exists():
            procedure = Procedure.objects.get(name=name)
            procedure_serializer = ProcedureSerializer(procedure, data=procedure_data, partial=True)
            helper.printMessage('DEBUG', 'merger.saveTender', "+++ Procedure already exists. Skipping.")
        else:
            procedure_serializer = ProcedureSerializer(data=procedure_data)
            helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Procedure to be created: {name}")
            procedure_serializer.is_valid(raise_exception=True)
            procedure = procedure_serializer.save()


    # Step x: Create or update Tender
    chrono = validated_data.get('chrono')
    tender = None
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Tender ... ")
    if chrono and Tender.objects.filter(chrono=chrono).exists():
        tender = Tender.objects.get(chrono=chrono)
        tender_serializer = TenderSerializer(tender, data=validated_data, partial=True)
        helper.printMessage('DEBUG', 'merger.saveTender', "+++ Tender already exists. Updating.")
    else:
        tender_serializer = TenderSerializer(data=validated_data)
        helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Tender to be created: {chrono}")
    tender_serializer.is_valid(raise_exception=True)
    tender = tender_serializer.save(category=category, client=client, kind=kind, mode=mode, procedure=procedure)
    

    # Step x: Handle Domains (many-to-many)
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Domains ... ")
    domains_data = formatted_data['domains']
    json_domain_keys = set()
    for domain_data in domains_data:
        name = domain_data.get('name')
        domain = None
        if name and Domain.objects.filter(name=name).exists():
            domain = Domain.objects.get(name=name)
            domain_serializer = DomainSerializer(domain, data=domain_data, partial=True)
            helper.printMessage('DEBUG', 'merger.saveTender', "+++ Domain of Activiry already exists. Skipping.")
        else:
            domain_serializer = DomainSerializer(data=domain_data)
            helper.printMessage('DEBUG', 'merger.saveTender', f"+++ Domain of Activiry to be created: {name}")
            domain_serializer.is_valid(raise_exception=True)
            domain = domain_serializer.save()
        json_domain_keys.add((domain.name))
        RelDomainTender.objects.get_or_create(domain=domain, tender=tender)


    # Remove domains not in JSON
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Domains relationships ... ")
    existing_domains = set(tender.domains.values_list('name'))
    domains_to_remove = existing_domains - json_domain_keys
    for name in domains_to_remove:
        domain = Domain.objects.filter(name=name).first()
        if domain:
            helper.printMessage('DEBUG', 'merger.saveTender', f"#### Unlinking Tender {tender.chrono} and Domain {domain.name} ... ")
            RelDomainTender.objects.filter(domain=domain, tender=tender).delete()


    # Step x: Handle Lots
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Lots ... ")
    lots_data = formatted_data["lots"]
    json_lot_keys = set()
    new_lots = []


    estimate_total, bond_total = 0, 0
    reserved_tender, variant_tender = False, False
    ll = len(lots_data)
    if ll > 0:
        helper.printMessage('TRACE', 'merger.saveTender', f"#### Got data for {ll} Lots. ")
        i = 0
        l1 = lots_data[0]
        reserved_tender = l1["reserved"]
        variant_tender = l1["variant"]

    for lot_data in lots_data:
        i += 1
        helper.printMessage('DEBUG', 'merger.saveTender', f"#### Handling Lot {i}/{ll} ... ")
        # Update Tender fields
        estimate_total += lot_data["estimate"]
        bond_total += lot_data["bond"]

        # Handle nested Category for Lot
        lot_category_data = lot_data["category"]
        lot_category = None
        helper.printMessage('DEBUG', 'merger.saveTender', f"#### Handling Lot Categories {i}/{ll} ... ")
        if lot_category_data:
            label = lot_category_data.get('label')
            if label and Category.objects.filter(label=label).exists():
                helper.printMessage('TRACE', 'merger.saveTender', "#### Lot Category exists. Skipping.")
                lot_category = Category.objects.get(label=label)
                lot_category_serializer = CategorySerializer(lot_category, data=lot_category_data, partial=True)
            else:
                lot_category_serializer = CategorySerializer(data=lot_category_data)
                helper.printMessage('TRACE', 'merger.saveTender', f"#### Lot Category to be created: {label}")
                lot_category_serializer.is_valid(raise_exception=True)
                lot_category = lot_category_serializer.save()

        meetings_data = lot_data['meetings']
        agrements_data = lot_data['agrements']
        qualifs_data = lot_data['qualifs']

        lot_data['category'] = lot_category

        # Match Lot by title
        lot_title = lot_data.get('title')
        lot = None
        helper.printMessage('TRACE', 'merger.saveTender', "#### Handling Lot ... ")
        if lot_title and Lot.objects.filter(title=lot_title, tender=tender).exists():
            helper.printMessage('TRACE', 'merger.saveTender', "#### Lot exists. Skipping.")
            lot = Lot.objects.get(title=lot_title, tender=tender)
            lot_serializer = LotSerializer(lot, data=lot_data, partial=True)
        else:
            lot_serializer = LotSerializer(data=lot_data)
            helper.printMessage('TRACE', 'merger.saveTender', f"#### Lot to be created: {lot_title}")
            lot_serializer.is_valid(raise_exception=True)
            lot = lot_serializer.save(tender=tender)

        json_lot_keys.add((lot.title, lot.number))

        # Handle Meetings
        json_meeting_keys = set()
        helper.printMessage('TRACE', 'merger.saveTender', "#### Handling Lot Meetings ... ")
        for meeting_data in meetings_data:
            when = meeting_data.get('when')
            description = meeting_data.get('description')
            json_meeting_keys.add((when, description))
            meeting = None
            if when and Meeting.objects.filter(when=when, lot=lot).exists():
                helper.printMessage('TRACE', 'merger.saveTender', "#### Meeting exists. Skipping.")
                meeting = Meeting.objects.get(when=when, lot=lot)
                meeting_serializer = MeetingSerializer(meeting, data=meeting_data, partial=True)
            else:
                meeting_serializer = MeetingSerializer(data=meeting_data)
                helper.printMessage('TRACE', 'merger.saveTender', f"#### Meeting to be created: {when}")
                meeting_serializer.is_valid(raise_exception=True)
                meeting_serializer.save(lot=lot)

        # Remove Meetings not in JSON
        helper.printMessage('TRACE', 'merger.saveTender', "### Handling Meetings relationships ... ")
        existing_meetings = set(lot.meetings.values_list('when', 'description'))
        meetings_to_remove = existing_meetings - json_meeting_keys
        for when, description in meetings_to_remove:
            Meeting.objects.filter(when=when, description=description, lot=lot).delete()

        # Handle Agrements (many-to-many)
        json_agrement_keys = set()
        helper.printMessage('TRACE', 'merger.saveTender', "#### Handling Lot Agrements ... ")
        for agrement_data in agrements_data:
            name = agrement_data.get('name')
            agrement = None
            if name and Agrement.objects.filter(name=name).exists():
                helper.printMessage('TRACE', 'merger.saveTender', "#### Agrement exists. Skipping.")
                agrement = Agrement.objects.get(name=name)
                agrement_serializer = AgrementSerializer(agrement, data=agrement_data, partial=True)
            else:
                agrement_serializer = AgrementSerializer(data=agrement_data)
                helper.printMessage('TRACE', 'merger.saveTender', f"#### Agrement to be created: {name}")
                agrement_serializer.is_valid(raise_exception=True)
                agrement = agrement_serializer.save()
            json_agrement_keys.add((agrement.short, agrement.name))
            RelAgrementLot.objects.get_or_create(agrement=agrement, lot=lot)

        # Remove Agrements not in JSON
        helper.printMessage('TRACE', 'merger.saveTender', "### Handling Agrements relationships ... ")
        existing_agrements = set(lot.agrements.values_list('short', 'name'))
        agrements_to_remove = existing_agrements - json_agrement_keys
        for short, name in agrements_to_remove:
            agrement = Agrement.objects.filter(short=short, name=name).first()
            if agrement:
                RelAgrementLot.objects.filter(agrement=agrement, lot=lot).delete()

        # Handle Qualifs (many-to-many)
        json_qualif_keys = set()
        helper.printMessage('TRACE', 'merger.saveTender', "#### Handling Lot Qualifs ... ")
        for qualif_data in qualifs_data:
            short = qualif_data.get('short')
            name = qualif_data.get('name')
            qualif = None
            if name and Qualif.objects.filter(name=name).exists():
                helper.printMessage('TRACE', 'merger.saveTender', "#### Qualif exists. Skipping.")
                qualif = Qualif.objects.get(name=name)
                qualif_serializer = QualifSerializer(qualif, data=qualif_data, partial=True)
            else:
                qualif_serializer = QualifSerializer(data=qualif_data)
                helper.printMessage('TRACE', 'merger.saveTender', f"#### Qualif to be created: {name}")
                qualif_serializer.is_valid(raise_exception=True)
                qualif = qualif_serializer.save()
            json_qualif_keys.add((qualif.short, qualif.name))
            RelQualifLot.objects.get_or_create(qualif=qualif, lot=lot)

        # Remove Qualifs not in JSON
        helper.printMessage('TRACE', 'merger.saveTender', "### Handling Qualifs relationships ... ")
        existing_qualifs = set(lot.qualifs.values_list('short', 'name'))
        qualifs_to_remove = existing_qualifs - json_qualif_keys
        for short, name in qualifs_to_remove:
            qualif = Qualif.objects.filter(name=name).first()
            if qualif:
                RelQualifLot.objects.filter(qualif=qualif, lot=lot).delete()

        new_lots.append(lot)
    
    # Update totals for Tender
    helper.printMessage('DEBUG', 'merger.saveTender', "### Updating Tender details from Lots ... ")
    tender = tender_serializer.save(estimate=estimate_total, bond = bond_total, reserved = reserved_tender, variant = variant_tender)
    
    # Remove Lots not in JSON
    helper.printMessage('TRACE', 'merger.saveTender', "### Handling Lots relationships ... ")
    existing_lots = set(tender.lots.values_list('title', 'number'))
    lots_to_remove = existing_lots - json_lot_keys
    for title, number in lots_to_remove:
        Lot.objects.filter(title=title, number=number, tender=tender).delete()

    return tender

