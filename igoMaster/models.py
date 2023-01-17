from django.db import models
import simplejson as Json
from .exceptions import *
import ast

# Create your models here.

####    TYPE D'UTILISATEUR
class UserType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'createdAt': self.createdAt
        }

    def get_members(self):
        return [
            u.to_json() for u in User.objects.filter(Type=self.id)
        ]

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
    JoinedAt=models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self) -> str:
        return self.FName

    @property
    def photo_url(self):
        if self.Photo and hasattr(self.Photo, 'url'):
            return self.Photo.url
        else:
            return "/static/IMG/blank-dark.svg"

    def to_json(self):
        #   RENVOIE LES INFOS DU USER AU FORMAT JSON
        return {
            'id': self.id,
            'last_name': self.LName,
            'first_name': self.FName,
            'email': self.Email,
            'phone': self.Phone,
            'password': self.Pass,
            'type': self.Type.to_json(),
            'photo_url': self.photo_url,
            'joined_at': self.JoinedAt
        }

    def get_etablishments(self):
        #   RENVOIE LA LISTE DES ETABLISSEMENTS DU USER
        return [
            e.to_json() for e in Etablishment.objects.filter(owner=self.id)
        ]

    def get_notifications(self):
        return [
            n.to_json() for n in Notification.objects.filter(toUser=self.id)
        ]

    def get_mails(self):
        return [
            m.to_json() for m in ContactMail.objects.filter(toUser=self.id)
        ]

    def get_favoris(self):
        # RENVOIE LA LISTE DES FAVORIS DU USER

        return Favoris.objects.get(user=self.id).get_etablishments()

    def add_favoris(self,eid):
        # AJOUTE L'ID DE L'ETABLISSEMENT AUX FAVORIS DU USER

        try:
            #   VERIFIER SI L'ETABLISSEMENT EXISTE
            e=Etablishment.objects.get(id=eid)

            # VERIFIER SI LE USER A DES FAVORIS
            try:
                uf=Favoris.objects.get(user=self.id)
                # ALORS ON L'AJOUTE
                uf.add(e.id)
            except:
                # LE FAVORIS N'EXISTE PAS 
                # ALORS ON LE CRÉ ET ON AJOUTE L'ETABLISSEMENT
                f=Favoris.objects.create(
                    user=self
                )
                f.add(e.id)

            return {
                    'added':True
                }
        except:
            # L'ETABLISSEMENT N'EXISTE PAS
            return ObjectNotFoundException('ETABLISHMENT',eid).format()

    def remove_favoris(self,eid):
        # SUPPRIME L'ETABLISSEMENT DES FAVORIS DU USER

        try:
            # VERIFIER SI L'ETABLISSEMENT EXISTE
            e=Etablishment.objects.get(id=eid)

            # VERIFIER SI LE USER A DES FAVORIS
            try:
                uf=Favoris.objects.get(user=self.id)
                # ALORS ON L'AJOUTE
                uf.remove(e.id)
            except:
                # LE FAVORIS N'EXISTE PAS 
                # ALORS ON LE CRÉ ET ON PASSE
                Favoris.objects.create(
                    user=self
                )

            return {
                    'removed':True
                }
        except:
            # L'ETABLISSEMENT N'EXISTE PAS
            return ObjectNotFoundException('ETABLISHMENT',eid).format()


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

    def to_Json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'image': self.image,
            'createdAt': self.createdAt
        }

    def get_subtypes(self):
        #   RENVOIE LA LISTE DES SOUS-CATÉGORIES DE LA CATÉGORIE

        return [
            s.to_json() for s in EtablishmentSubType.objects.filter(type__id=self.id)
        ] 

    def get_etablishments(self):
        #   RENVOIE LA LISTE DES ETABLISSEMENTS DU MEME TYPE
        return [
            e.to_json() for e in Etablishment.objects.filter(subType__type=self.id)
        ]

####    SOUS-TYPES D'ETABLISSEMENTS
class EtablishmentSubType(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    type=models.ForeignKey("EtablishmentType",on_delete=models.CASCADE)
    image=models.CharField(max_length=150,default='AUCUNE IMAGE')
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type.to_json(),
            'image': self.image,
            'createdAt': self.createdAt
        }

    def get_etablishments(self):
        return [
            e.to_json() for e in Etablishment.objects.filter(subType=self.id)
        ]

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

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'region': self.region,
            'country': self.country,
            'createdAt': self.createdAt
        }

    def get_etablishments(self):
        return [
            e.to_json() for e in Etablishment.objects.filter(city__id=self.id)
        ]

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

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'presentation': self.presentation,
            'address': self.address,
            'tags': self.tags,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'postal': self.postal,
            'isActive': self.isActive,
            'city': self.city.to_json(),
            'subType': self.subType.to_json(),
            'owner': self.owner.to_json(),
            'createdAt': self.createdAt
        }

    def get_medias(self):
        return [
            m.to_json() for m in Media.objects.filter(etablishment=self.id)
        ]

    def get_subscriptions(self):
        return [
            s.to_json() for s in Subscription.objects.filter(etablishment=self.id)
        ]

    def get_contacts(self):
        return [
            c.to_json() for c in Contact.objects.filter(etablishment=self.id)
        ]

    def get_socials(self):
        return [
            s.to_json() for s in Social.objects.filter(etablishment=self.id)
        ]

    def get_others(self):
        try:
            return OTHER.objects.get(etablishment=self.id).to_json()
        except:
            return ObjectNotFoundException(
                "OTHER's Etablishment",
                self.id
            ).format()

    def get_promotions(self):
        try:
            return Promotion.objects.get(etablishment=self.id).to_json()
        except:
            return ObjectNotFoundException(
                "PROMOTION's Etablishment",
                self.id
            ).format()

####    MEDIAS
class Media(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=150)
    image=models.ImageField()
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def img_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/IMG/balade igoguide.jpg"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.img_url,
            'createdAt': self.createdAt,
            'etablishment': self.etablishment.to_json()
        }


####    CONTACTS
class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    telephone=models.CharField(max_length=20)
    email=models.CharField(max_length=150)
    website=models.CharField(max_length=300)
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def to_json(self):
        return {
            'id': self.id,
            'telephone': self.telephone,
            'email': self.email,
            'website': self.website,
            'createdAt': self.createdAt,
            'etablishment':self.etablishment.to_json()
        }

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

    def to_json(self):
        return {
            'id': self.id,
            'content': Json.load(self.content),
            'etablishment': self.etablishment.to_json()
        }

####    SOCIALS
class Social(models.Model):
    id=models.AutoField(primary_key=True)
    facebookName=models.CharField(max_length=500)
    instagramName=models.CharField(max_length=500)
    tweeterName=models.CharField(max_length=500,default='Non renseigné')
    tiktokName=models.CharField(max_length=500,default='Non renseigné')
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def to_json(self):
        return {
            'id': self.id,
            'facebookName': self.facebookName,
            'instagramName': self.instagramName,
            'tweeterName': self.tweeterName,
            'tiktokName': self.tiktokName,
            'createdAt': self.createdAt,
            'etablishment': self.etablishment.to_json()
        }

####    FAVORIS
class Favoris(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey("User",on_delete=models.CASCADE,null=True,blank=True)
    etablishments=models.TextField(default="[]")#models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def load_objects(self):
        return ast.literal_eval(self.etablishments)

    def add(self,id):
        x=str(self.load_objects())
        if id not in x:
            x.append(id)
            self.etablishments=str(x)
            self.save()

    def remove(self,id):
        #   SUPPRIME L'ETABLI
        x=list(self.load_objects())
        if id in x:
            x.remove(id)
            self.etablishments=str(x)
            self.save()

    def get_etablishments(self):
        # RENVOIE LES ETABLISSEMENTS CONTENUS DANS LE FAVORIS

        l=[]
        for i in self.load_objects():
            #   SI L'ETABLISSEMENT EXISTE!
            try:
                #   COOL!
                l.append(Etablishment.objects.get(user=i).to_json())
            except :
                #   L'ETABLISSEMENT N'EXISTE PAS!
                pass    #   ON ZAPPE!
        return l

####    ABONNEMENTS
class Subscription(models.Model):
    id=models.AutoField(primary_key=True)
    isActiive=models.BooleanField(default=False)    # Si l'abonnement est actif
    activeDuration=models.IntegerField(default=1)   # Durée en mois (1 mois gratuit par defaut )
    fee=models.FloatField(default=49.0)             # Côut de l'abonnement 49.0€ par defaut
    stopDate=models.DateField(auto_now_add=False)   # Date de fin d'abonnements
    etablishment=models.ForeignKey("Etablishment",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def to_json(self):
        return {
            'id': self.id,
            'isActive': self.isActive,
            'activeDuration': self.activeDuration,
            'fee': self.fee,
            'startDate': self.stopDate,
            'createdAt': self.createdAt,
            'etablishment': self.etablishment.to_json()
        }

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

    def to_json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'subscription': self.subscription.to_json(),
            'status': self.status,
            'createdAt': self.createdAt
        }

####    NOTIFICATIONS
class Notification(models.Model):
    id=models.AutoField(primary_key=True)
    message=models.CharField(max_length=2000)
    isOpened=models.BooleanField(default=False)
    fromUser=models.CharField(max_length=200)
    toUser=models.ForeignKey("User",on_delete=models.CASCADE)
    createdAt=models.DateField(auto_now_add=True)

    def to_json(self):
        return {
            'id': self.id,
            'message': self.message,
            'isOpened': self.isOpened,
            'fromUser': self.fromUser,
            'toUser': self.toUser.to_json(),
            'createdAt': self.createdAt
        }

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

    def to_json(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'email': self.email,
            'message': self.message,
            'isOpened': self.isOpened,
            'fromUser': self.get_fromUser(),
            'toUser': self.toUser.to_json(),
            'createdAt': self.createdAt
        }

    def get_fromUser(self):
        return User.objects.get(id=self.fromUser).to_json()

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

    def to_json(self):
        return {
            'id': self.id,
            'duration': self.duration,
            'text': self.text,
            'fee': self.fee,
            'stopDate': self.stopDate,
            'isActive': self.isActive,
            'createdAt': self.createdAt,
            'etablishment': self.etablishment.to_json()
        }

###     PACKS DE FORFAITS
class Forfait(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    price=models.FloatField(default=25)
    duration=models.IntegerField(default=1) # Durée de visibilité

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'duration': self.duration
        }

###     BANIERES
class Banner(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500)
    image=models.ImageField()

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return "/static/IMG/balade igoguide.jpg"

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image_url
        }