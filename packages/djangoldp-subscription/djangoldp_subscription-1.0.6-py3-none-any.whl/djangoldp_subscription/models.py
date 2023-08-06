from django.core.mail import send_mail
from django.db import models
from djangoldp.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader
from datetime import datetime

class Typemember (Model):
    name = models.CharField(max_length=50, verbose_name="Type of member")

    def __str__(self):
        return self.name 

class Gendermember (Model):
    name = models.CharField(max_length=50, verbose_name="Member gender")

    def __str__(self):
        return self.name 

class Member (Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    firstname = models.CharField(max_length=50, blank=True, null=True, verbose_name="First name")
    typemember = models.ForeignKey(Typemember,max_length=50, verbose_name="Type of member", null=True, on_delete=models.SET_NULL)
    gender = models.ForeignKey(Gendermember, blank=True, null=True, max_length=50, on_delete=models.SET_NULL)
    email = models.CharField(max_length=50, verbose_name="Email") 
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    birthdate = models.DateField(blank=True, null=True, verbose_name="Birth date")
    birthcity = models.CharField(max_length=50, blank=True, null=True, verbose_name="Birth city")
    birthcountry = models.CharField(max_length=50, blank=True, null=True, verbose_name="Birth country")
    corponame = models.CharField(max_length=50, blank=True, null=True,verbose_name="Corporate Name")
    mandat = models.CharField(max_length=50, blank=True, null=True,verbose_name="Social mandate")
    siret = models.CharField(max_length=15, blank=True, null=True, verbose_name="Siret")
    numberaddress = models.CharField(max_length=10, verbose_name="Street number")
    streetaddress = models.CharField(max_length=50, verbose_name="Street name")
    zipcode = models.CharField(max_length=10, verbose_name="Zip code")
    cityaddress = models.CharField(max_length=50, verbose_name="City")
    countryaddress = models.CharField(max_length=50, verbose_name="Country")
    mailacceptance = models.BooleanField(verbose_name="acceptance of notification emails")
    changemail = models.BooleanField(verbose_name="Change email validation")
    informationvalidation = models.BooleanField(verbose_name="Risk validation")
    statutes = models.BooleanField(verbose_name="Knowledge of the statutes")
    cavalidation = models.BooleanField(verbose_name="Validation of the CA")
    servicesattestation = models.BooleanField(verbose_name="Attestation of services provided", default=False)
    beneficiciaireconfirmation  = models.BooleanField(verbose_name="Bénéficiaire subscription")
    partquantity = models.IntegerField(verbose_name="Part Quantity")
    iddocument = models.URLField(blank=True, null=True, verbose_name="ID")
    subscriptiondate = models.DateTimeField(default=datetime.now, blank=True, null=True, verbose_name="Subscription date")

    class Meta : 
        anonymous_perms = ['view', 'add', 'change']

    def __str__(self):
        return self.name 

@receiver(post_save, sender=Member)
def send_email_on_contact(sender, instance, created, **kwargs):
    if created:
       message = loader.render_to_string('souscripteur_email.txt', {'member': instance})
       send_mail('Nous avons bien reçu ta demande de souscription', message, 'salut@startinblox.com', {instance.email})

