import uuid
from django.db import models


class Agrement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'agrement'


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=32, blank=True, null=True)
    # rank = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'category'


class Change(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tender = models.ForeignKey('Tender', on_delete=models.DO_NOTHING, related_name="changes", db_column='tender', blank=True, null=True)    
    reported = models.DateTimeField(blank=True, null=True)
    field = models.CharField(max_length=64, blank=True, null=True)
    old_val = models.CharField(max_length=256, blank=True, null=True)
    new_val = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'change'


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    ministery = models.CharField(max_length=16, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'client'


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    utilizer = models.ForeignKey('Utilizer', on_delete=models.DO_NOTHING, related_name="contacts", db_column='utilizer', blank=True, null=True)

    class Meta:
        db_table = 'contact'


class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'domain'


class Download(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    when = models.DateTimeField(blank=True, null=True)
    bytes_media = models.BigIntegerField(blank=True, null=True)
    ua = models.CharField(max_length=256, blank=True, null=True)
    ip = models.CharField(max_length=48, blank=True, null=True)
    tender = models.ForeignKey('Tender', on_delete=models.DO_NOTHING, related_name="downloads", db_column='tender', blank=True, null=True)
    utilizer = models.ForeignKey('Utilizer', on_delete=models.DO_NOTHING, related_name="downloads", db_column='utilizer', blank=True, null=True)

    class Meta:
        db_table = 'download'


class Favo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    when = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True, null=True)
    ua = models.CharField(max_length=256, blank=True, null=True)
    ip = models.CharField(max_length=48, blank=True, null=True)
    utilizer = models.ForeignKey('Utilizer', on_delete=models.DO_NOTHING, related_name="favos", db_column='utilizer', blank=True, null=True)
    tender = models.ForeignKey('Tender', on_delete=models.DO_NOTHING, related_name="favos", db_column='tender', blank=True, null=True)

    class Meta:
        db_table = 'favo'


class Lot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank=True, null=True)
    
    estimate = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    bond = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    # plans_price = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    reserved = models.BooleanField(blank=True, null=True)
    variant = models.BooleanField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="lots", db_column='category', blank=True, null=True)
    
    tender = models.ForeignKey('Tender', on_delete=models.DO_NOTHING, related_name="lots", db_column='tender', blank=True, null=True)
    agrements = models.ManyToManyField('Agrement', through='RelAgrementLot', related_name='lots')
    qualifs = models.ManyToManyField('Qualif', through='RelQualifLot', related_name='lots')

    class Meta:
        db_table = 'lot'
        ordering = ['number']


class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    when = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    lot = models.ForeignKey(Lot, on_delete=models.DO_NOTHING, related_name="meetings", db_column='lot', blank=True, null=True)

    class Meta:
        db_table = 'meeting'


class Mode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'mode'


class Procedure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'procedure'


class Qualif(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    classe = models.CharField(max_length=8, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'qualif'


class RelAgrementLot(models.Model):
    pk = models.CompositePrimaryKey('agrement', 'lot')
    agrement = models.ForeignKey(Agrement, on_delete=models.DO_NOTHING, db_column='agrement')
    lot = models.ForeignKey(Lot, on_delete=models.DO_NOTHING, db_column='lot')

    class Meta:
        db_table = 'rel_agrement_lot'
        unique_together = ('agrement', 'lot')


class RelDomainTender(models.Model):
    pk = models.CompositePrimaryKey('domain', 'tender')
    domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING, db_column='domain')
    tender = models.ForeignKey('Tender', on_delete=models.DO_NOTHING, db_column='tender')

    class Meta:
        db_table = 'rel_domain_tender'
        unique_together = ('domain', 'tender')


class RelQualifLot(models.Model):
    pk = models.CompositePrimaryKey('qualif', 'lot')
    qualif = models.ForeignKey(Qualif, on_delete=models.DO_NOTHING, db_column='qualif')
    lot = models.ForeignKey(Lot, on_delete=models.DO_NOTHING, db_column='lot')

    class Meta:
        db_table = 'rel_qualif_lot'
        unique_together = ('qualif', 'lot')


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    lot = models.ForeignKey(Lot, on_delete=models.DO_NOTHING, related_name="samples", db_column='lot', blank=True, null=True)

    class Meta:
        db_table = 'sample'


class Tender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chrono = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    reference = models.CharField(max_length=128, blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    lots_count = models.SmallIntegerField(blank=True, null=True)
    estimate = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    bond = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    plans_price = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    reserved = models.BooleanField(blank=True, null=True)
    variant = models.BooleanField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="tenders", db_column='category', blank=True, null=True)

    location = models.CharField(max_length=256, blank=True, null=True)
    ebid = models.SmallIntegerField(blank=True, null=True, db_comment='1: Required, 0: Not required, Else: NA')
    esign = models.SmallIntegerField(blank=True, null=True, db_comment='1: Required, 0: Not required, Else: NA')
    size_read = models.CharField(max_length=32, blank=True, null=True)
    size_bytes = models.BigIntegerField(blank=True, null=True)
    address_withdrawal = models.CharField(max_length=512, blank=True, null=True)
    address_bidding = models.CharField(max_length=512, blank=True, null=True)
    address_opening = models.CharField(max_length=512, blank=True, null=True)
    contact_name = models.CharField(max_length=64, blank=True, null=True)
    contact_phone = models.CharField(max_length=64, blank=True, null=True)
    contact_email = models.CharField(max_length=64, blank=True, null=True)
    contact_fax = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    cancelled = models.BooleanField(blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)
    acronym = models.CharField(max_length=4, blank=True, null=True)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, related_name='tenders', db_column='mode', blank=True, null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.DO_NOTHING, related_name='tenders', db_column='procedure', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='tenders', db_column='client', blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.DO_NOTHING, related_name='tenders', db_column='type', blank=True, null=True)
    domains = models.ManyToManyField('Domain', through='RelDomainTender', related_name='tenders')

    class Meta:
        db_table = 'tender'
    
    def __str__():
        return self.title

    # def save(self, , *args, **kwargs):
    #     self.estimate = 0
    #     self.bond = 0
    #     self.plans_price = 0
    #     self.reserved = False
    #     self.variant = False
    #     self.category = None

        # return super().save(*args, **kwargs)


class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'type'


class Utilizer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=64)
    email = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'utilizer'


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    when = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)
    lot = models.ForeignKey(Lot, on_delete=models.DO_NOTHING, related_name="visits", db_column='lot', blank=True, null=True)

    class Meta:
        db_table = 'visit'

