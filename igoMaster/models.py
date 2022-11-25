from django.db import models

# Create your models here.

####    TYPE D'UTILISATEUR
class UserType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

####    UTILISATEURS
class User(models.Model):
    id=models.AutoField(primary_key=True)
    LName=models.CharField(max_length=50)
    FName=models.CharField(max_length=80)
    Email=models.EmailField(max_length=150,unique=True)
    Phone=models.CharField(max_length=20)
    Pass=models.CharField(max_length=25)
    Type=models.ForeignKey("UserType",on_delete=models.CASCADE)
    Photo=models.ImageField(default='blank-dark.svg',blank=True,null=True)
    JoinedAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.FName

####    TYPE D'ETABLISSEMENTS
class EtablishmentType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    color=models.CharField(max_length=20,default='#FFFFFF')
    image=models.CharField(max_length=150,default='AUCUNE IMAGE')
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

####    SOUS-TYPES D'ETABLISSEMENTS
class EtablishmentSubType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    type=models.ForeignKey("EtablishmentType",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

####    VILLES
class City(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    department=models.CharField(max_length=250)
    region=models.CharField(max_length=250)
    country=models.CharField(max_length=250,default='FRANCE')
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

####    ETABLISSEMENTS
class Etablishment(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    presentation=models.CharField(max_length=1500)
    address=models.CharField(max_length=500)
    tags=models.CharField(max_length=2000)
    longitude=models.FloatField(default=0.0)
    latitude=models.FloatField(default=0.0)
    postal=models.CharField(max_length=100,blank=True)
    isActive=models.BooleanField(default=True)
    city=models.ForeignKey("City",on_delete=models.CASCADE)
    subType=models.ForeignKey("EtablishmentSubType",on_delete=models.CASCADE)
    owner=models.ForeignKey("User",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def truncate(self) -> str:
        return self.presentation[:90] if len(self.presentation)>90 else self.presentation

####    MEDIAS
class Media(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=150)
    image=models.ImageField()
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

####    CONTACTS
class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    telephone=models.CharField(max_length=20)
    email=models.CharField(max_length=150)
    website=models.CharField(max_length=300)
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

####    ACTIVITES
class Activite(models.Model):
    id=models.AutoField(primary_key=True)
    children=models.CharField(max_length=500)   #Adapté aux enfants?
    pets=models.CharField(max_length=500)       #Acceptation des animaux?
    handicaps=models.CharField(max_length=500)  #Acceptation des handicapés?
    breakfast=models.CharField(max_length=500)  #Petit dej gratuit?
    difficults=models.CharField(max_length=500) #Difficultés de l'activité
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

####    SUPPLEMENTS
class OTHER(models.Model):
    id=models.AutoField(primary_key=True)
    content=models.CharField(max_length=10000,null=True)
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)

####    SOCIALS
class Social(models.Model):
    id=models.AutoField(primary_key=True)
    facebookName=models.CharField(max_length=500)
    instagramName=models.CharField(max_length=500)
    tweeterName=models.CharField(max_length=500,default='Non renseigné')
    tiktokName=models.CharField(max_length=500,default='Non renseigné')
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

####    FAVORIS
class Favoris(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey("User",on_delete=models.CASCADE)
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

####    ABONNEMENTS
class Subscription(models.Model):
    id=models.AutoField(primary_key=True)
    isActiive=models.BooleanField(default=False)    # Si l'abonnement est actif
    activeDuration=models.IntegerField(default=1)   # Durée en mois (1 mois gratuit par defaut )
    fee=models.FloatField(default=49.0)             # Côut de l'abonnement 49.0€ par defaut
    stopDate=models.DateField(auto_now_add=False)   # Date de fin d'abonnements
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def isPaied(self):
        try:
            Payment.objects.get(subscription=self.id,status="SUCCESS")
            return True
        except:
            return False

####    PAIEMENTS
class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    amount=models.FloatField(default=0.0)
    status=models.CharField(max_length=20)
    subscription=models.ForeignKey("Subscription",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

####    NOTIFICATIONS
class Notification(models.Model):
    id=models.AutoField(primary_key=True)
    message=models.CharField(max_length=2000)
    isOpened=models.BooleanField(default=False)
    fromUser=models.CharField(max_length=200)
    toUser=models.ForeignKey("User",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

####    MAILS
class ContactMail(models.Model):
    id=models.AutoField(primary_key=True)
    subject=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    message=models.CharField(max_length=2000)
    isOpened=models.BooleanField(default=False)
    fromUser=models.IntegerField()
    toUser=models.ForeignKey("User",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)   #To DateTimeField

###     PROMOTIONS
class Promotion(models.Model):
    id=models.AutoField(primary_key=True)
    duration=models.IntegerField(default=1)
    text=models.CharField(max_length=2000,default='Non renseigné')
    fee=models.FloatField(default=0.0)
    stopDate=models.DateField(auto_now_add=False)
    isActive=models.BooleanField(default=True)
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

###     PACKS DE FORFAITS
class Forfait(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    price=models.FloatField(default=25)
    duration=models.IntegerField(default=1) # Durée de visibilité

    def __str__(self):
        return self.name

###     BANIERES
class Banner(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.ImageField()