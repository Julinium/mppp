# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Agrement(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'agrement'


class Category(models.Model):
    id = models.UUIDField(primary_key=True)
    label = models.CharField(max_length=32, blank=True, null=True)
    rank = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'category'


class Change(models.Model):
    id = models.UUIDField(primary_key=True)
    reported = models.DateTimeField(blank=True, null=True)
    field = models.CharField(max_length=64, blank=True, null=True)
    old_val = models.CharField(max_length=256, blank=True, null=True)
    new_val = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'change'


class Client(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    ministery = models.CharField(max_length=16, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'client'


class Contact(models.Model):
    id = models.UUIDField(primary_key=True)
    when = models.DateTimeField(blank=True, null=True)
    ua = models.CharField(max_length=256, blank=True, null=True)
    ip = models.CharField(max_length=48, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    message = models.CharField(max_length=1024, blank=True, null=True)
    method = models.CharField(max_length=8, blank=True, null=True)
    newsletter = models.BooleanField(blank=True, null=True)
    promos = models.BooleanField(blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True, null=True)
    actions = models.CharField(max_length=512, blank=True, null=True)
    solved = models.BooleanField(blank=True, null=True)
    file = models.CharField(max_length=512, blank=True, null=True)
    id_utilizer = models.ForeignKey('Utilizer', models.DO_NOTHING, db_column='id_utilizer', blank=True, null=True)

    class Meta:
        db_table = 'contact'


class Domain(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'domain'


class Download(models.Model):
    id = models.UUIDField(primary_key=True)
    when = models.DateTimeField(blank=True, null=True)
    bytes_media = models.BigIntegerField(blank=True, null=True)
    ua = models.CharField(max_length=256, blank=True, null=True)
    ip = models.CharField(max_length=48, blank=True, null=True)
    id_tender = models.ForeignKey('Tender', models.DO_NOTHING, db_column='id_tender', blank=True, null=True)
    id_utilizer = models.ForeignKey('Utilizer', models.DO_NOTHING, db_column='id_utilizer', blank=True, null=True)

    class Meta:
        db_table = 'download'


class Favo(models.Model):
    id = models.UUIDField(primary_key=True)
    when = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True, null=True)
    ua = models.CharField(max_length=256, blank=True, null=True)
    ip = models.CharField(max_length=48, blank=True, null=True)
    id_utilizer = models.ForeignKey('Utilizer', models.DO_NOTHING, db_column='id_utilizer', blank=True, null=True)
    id_tender = models.ForeignKey('Tender', models.DO_NOTHING, db_column='id_tender', blank=True, null=True)

    class Meta:
        db_table = 'favo'


class Lot(models.Model):
    id = models.UUIDField(primary_key=True)
    number = models.SmallIntegerField()
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank=True, null=True)
    estimate = models.BigIntegerField(blank=True, null=True, db_comment='In cents')
    bond = models.BigIntegerField(blank=True, null=True)
    reserved = models.BooleanField(blank=True, null=True)
    variant = models.BooleanField(blank=True, null=True)
    plans_price = models.BigIntegerField(blank=True, null=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category', blank=True, null=True)
    id_tender = models.ForeignKey('Tender', models.DO_NOTHING, db_column='id_tender', blank=True, null=True)

    class Meta:
        db_table = 'lot'


class Meeting(models.Model):
    id = models.UUIDField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    id_lot = models.ForeignKey(Lot, models.DO_NOTHING, db_column='id_lot', blank=True, null=True)

    class Meta:
        db_table = 'meeting'


class Mode(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'mode'


class Procedure(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'procedure'


class Qualif(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    degree = models.CharField(max_length=8, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'qualif'


class RelAgrementLot(models.Model):
    pk = models.CompositePrimaryKey('id_agrement', 'id_lot')
    id_agrement = models.ForeignKey(Agrement, models.DO_NOTHING, db_column='id_agrement')
    id_lot = models.ForeignKey(Lot, models.DO_NOTHING, db_column='id_lot')

    class Meta:
        db_table = 'rel_agrement_lot'


class RelChangeTender(models.Model):
    pk = models.CompositePrimaryKey('id_change', 'id_tender')
    id_change = models.ForeignKey(Change, models.DO_NOTHING, db_column='id_change')
    id_tender = models.ForeignKey('Tender', models.DO_NOTHING, db_column='id_tender')

    class Meta:
        db_table = 'rel_change_tender'


class RelDomainTender(models.Model):
    pk = models.CompositePrimaryKey('id_domain', 'id_tender')
    id_domain = models.ForeignKey(Domain, models.DO_NOTHING, db_column='id_domain')
    id_tender = models.ForeignKey('Tender', models.DO_NOTHING, db_column='id_tender')

    class Meta:
        db_table = 'rel_domain_tender'


class RelQualifOt(models.Model):
    pk = models.CompositePrimaryKey('id_qualif', 'id_lot')
    id_qualif = models.ForeignKey(Qualif, models.DO_NOTHING, db_column='id_qualif')
    id_lot = models.ForeignKey(Lot, models.DO_NOTHING, db_column='id_lot')

    class Meta:
        db_table = 'rel_qualif_ot'


class Sample(models.Model):
    id = models.UUIDField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    id_lot = models.ForeignKey(Lot, models.DO_NOTHING, db_column='id_lot', blank=True, null=True)

    class Meta:
        db_table = 'sample'


class Tender(models.Model):
    id = models.UUIDField(primary_key=True)
    chrono = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    reference = models.CharField(max_length=128, blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    ebid = models.SmallIntegerField(blank=True, null=True, db_comment='1: Required, 0: Not required, Else: NA')
    esign = models.SmallIntegerField(blank=True, null=True, db_comment='1: Required, 0: Not required, Else: NA')
    size_read = models.CharField(max_length=32, blank=True, null=True)
    size_bytes = models.BigIntegerField(blank=True, null=True)
    address_withdrawal = models.CharField(max_length=512, blank=True, null=True)
    address_bidding = models.CharField(max_length=512, blank=True, null=True)
    address_awarding = models.CharField(max_length=512, blank=True, null=True)
    contact_name = models.CharField(max_length=64, blank=True, null=True)
    contact_phone = models.CharField(max_length=64, blank=True, null=True)
    contact_email = models.CharField(max_length=64, blank=True, null=True)
    contact_fax = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    cancelled = models.BooleanField(blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)
    id_mode = models.ForeignKey(Mode, models.DO_NOTHING, db_column='id_mode', blank=True, null=True)
    id_procedure = models.ForeignKey(Procedure, models.DO_NOTHING, db_column='id_procedure', blank=True, null=True)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client', blank=True, null=True)
    id_type = models.ForeignKey('Type', models.DO_NOTHING, db_column='id_type', blank=True, null=True)

    class Meta:
        db_table = 'tender'


class Type(models.Model):
    id = models.UUIDField(primary_key=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'type'


class Utilizer(models.Model):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(max_length=64)
    email = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'utilizer'


class Visit(models.Model):
    id = models.UUIDField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    id_lot = models.ForeignKey(Lot, models.DO_NOTHING, db_column='id_lot', blank=True, null=True)

    class Meta:
        db_table = 'visit'

