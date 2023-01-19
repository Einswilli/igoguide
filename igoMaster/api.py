from django.contrib.auth import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from igoMaster.exceptions import *
from igoMaster.services.authService import AuthService
import os
from igoMaster.services.bannerService import BannerService
from igoMaster.services.contactMailService import ContactMailService
from igoMaster.services.etablishmentService import EtablishmentService
from igoMaster.services.favoriService import FavorisService
from igoMaster.services.forfaitService import ForfaitServive
from igoMaster.services.mediaService import MediaService
from igoMaster.services.notificationService import NotificationsService
from igoMaster.services.paymentService import PaymentService
from igoMaster.services.promotionService import PromotionService
from igoMaster.services.subscriptionService import SubscriptionService
from igoMaster.services.userService import UserService
from igoMaster.services.userTypeService import UserTypeService

########
####    AUTHENTIFICATION
########
class AUTH:

    @csrf_exempt
    def login(self, request):
        # AUTHENTIFIE ET RENVOIE LE USER CORRESPONDANT

        if request.method=='POST':
            return JsonResponse(
                AuthService().login(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def reset_password(self, request):
        # RECUPERATION DE MOT DE PASSE

        if request.method=='POST':
            return JsonResponse(
                AuthService().pass_reset(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def send_password(self, request):
        # RENVOIE LE PASSWORD RECUPERE

        if request.method=='POST':
            return JsonResponse(
                AuthService().send_pass(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )


########
####    USERTYPE
########
class USERTYPE:

    @csrf_exempt
    def save(self,request):
        #   ENREGISTRE UN USERTYPE

        if request.method=='POST':
            return JsonResponse(
                UserTypeService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE LE USERTYPE AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                UserTypeService().show(id),
                safe=True
            ) 
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
        )

    @csrf_exempt
    def list(self,request):
        # RENVOIE LA LISTE DES USERTYPES

        if request.method=='GET':
            return JsonResponse(
                UserTypeService().list(),
                safe=True
            )

    @csrf_exempt
    def update(self,request,id):
        # METS A JOUR LE USERTYPE

        if request.method=='POST':
            return JsonResponse(
                UserTypeService().update(id,request)
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
        )

    @csrf_exempt
    def get_members(self,request,id):
        # RENVOIE LES MEMBRES USER DU USERTYPE AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                UserTypeService().get_members(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
        )


########
####    USERS
########
class USER:

    @csrf_exempt
    def save(self,request):
        # ENREGISTRE UN NOUVEU USER

        if request.method=='POST':
            return JsonResponse(
                UserService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
        )

    @csrf_exempt
    def update(self,request,id):
        #   METS A JOUR LE USER

        if request.method=='POST':
            return JsonResponse(
                UserService().update(request,id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE LE USER AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                UserService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def delete(self,request,id):
        # SUPPRIME LE USER AVEC L'ID

        if request.method=='DELETE':
            return JsonResponse(
                UserService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'DELETE').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        # RENVOIE LA LISTE DES USERS

        if request.method=='GET':
            return JsonResponse(
                UserService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_etablissements(self,request,id):
        # RENVOIE LES ETABLISSEMENTS DU USER AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                UserService().get_etablissements(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_notifications(self,request,id):
        # RENVOIE LES NOTIFICATIONS DU USER

        if request.method=='GET':
            return JsonResponse(
                UserService().get_notifications(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_mails(self,request,id):
        # RENVOIE LES MAILS DE CONTACT DU USER

        if request.method=='GET':
            return  JsonResponse(
                UserService().get_mails(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def add_favoris(self,request,uid,eid):
        # AJOUTE L'ETABLISSEMENTS AUX FAVORIS DU USER

        if request.method=='POST':
            return JsonResponse(
                UserService().add_favoris(uid,eid),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def remove_favoris(self,request,uid,eid):
        # SUPPRIME L'ETABLISSEMENT AVEC L'EID DES FAVORIS DU USER AVEC L'UID

        if request.method=='POST':
            return JsonResponse(
                UserService().remove_favoris(uid,eid),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def get_favoris(self,request,id):
        # RENVoIE LES FAVORIS DU USER AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                UserService().get_favoris(id)
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )


########
####    BANNERS
########
class BANNER:

    @csrf_exempt
    def save(self,request):
        # ENREGISTRE UNE NOUVELLE BANNIERE

        if request.method=='POST':
            return JsonResponse(
                BannerService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE LA BANNIERE AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                BannerService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method, 'GET').format(),
            safe=True
        )

    @csrf_exempt
    def delete(self,request,id):
        # SUPPRIME LA BANNIERE AVEC L'ID

        if request.method=='DELETE':
            return JsonResponse(
                BannerService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'DELETE').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        # RENVOIE LA LISTE DES BANNIERES

        if request.method=='GET':
            return JsonResponse(
                BannerService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )


########
####    CONTACTMAILS
########
class CONTACTMAIL:

    @csrf_exempt
    def save(self,request):
        # ENREGISTRE UN NOUVEUA MAIL DE CONTACT

        if request.method=='POST':
            return JsonResponse(
                ContactMailService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        # RENVOIE LA LISTE DES MAILS DE CONTACTS

        if request.method=='GET':
            return JsonResponse(
                ContactMailService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(), 
            safe=True
        )

    @csrf_exempt
    def get_user_mails(self,request,uid):
        # RENVOIE LES MAILS DE CONTACTS REÇUS PAR LE USER AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                ContactMailService().get_user_mails(uid),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_user_unread_mails(self,request,uid):
        # RENVOIE LES MAILS DE CONTACTS NON LUS DU USER AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                ContactMailService().get_user_unread_mails(uid),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE LE MAIL AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                ContactMailService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            saffe=True
        )

    @csrf_exempt
    def delete(self,request,id):
        # SUPPRIME LE MAIL AVEC L'ID

        if request.method=='DELETE':
            return JsonResponse(
                ContactMailService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'DELETE').format(),
        )

    
########
####    ETABLISHMENTS
########
class ETABLISHMENT:

    @csrf_exempt
    def save(self,request):
        # ENREGISTRE UN NOUVEL ETABLISSEMENT

        if request.method=='POST':
            return JsonResponse(
                EtablishmentService.save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE L'ETABLISSEMENT AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        #RENVOIE LA LISTE DES ETABLISSEMENTS

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def update(self,request,id):
        # MET A JOUR L'ETABLISSEMENT

        if request.method=='POST':
            return JsonResponse(
                EtablishmentService().update(request,id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def get_medias(self,request,id):
        # RENVOIE LES MEDIAS DE L'ETABLISSEMENT

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().get_medias(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_contacts(self,request,id):
        # RENVOIE LES CONTACTS DE L'ETABLISSEMENT

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().get_contacts(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_subscriptions(self,request,id):
        # RENVOIE LES SUBSCRIPTIONS DE L'ETABLISSEMENT

        if request.method=='GET':
            return  JsonResponse(
                EtablishmentService().get_subscriptions(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_socials(self,request,id):
        #   RENVOIE LES RESEAUX DE L'ETABLISSEMENT

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().get_socials(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_others(self,request,id):
        # RENVOIE LES OTHERS DE L'ETABLISSEMENT

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().get_others(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_promotions(self,request,id):
        # RENVOIE LES PROMOTIONS DE L'ETABLISSEMENT

        if request.method=='GET':
            return JsonResponse(
                EtablishmentService().get_promotions(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )


########
####    FAVORIS
########
class FAVORIS:

    @csrf_exempt
    def get_user(self,request,id):
        # RENVOIE LE LE USER ASSOCIE A UN FAVORI

        if request.method=='GET':
            return JsonResponse(
                FavorisService().get_user(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def add(self,request,fid,eid):
        # AJOUTE L'ETABLISSEMENT AU FAVORI AVEC LE FID

        if request.method=='POST':
            return JsonResponse(
                FavorisService().add(fid,eid),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def remove(self,request,fid,eid):
        # SUPPRIME L'ETABLISSEMENT DU FAVORI AVEC LE FID

        if request.method=='POST':
            return JsonResponse(
                FavorisService().remove(fid,eid),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def get_etablishment(self,request,fid):
        # RENVOIE LES ETABLISSEMENTS CONTENUS DANS LE FAVORI AVEC FID

        if request.method=='GET':
            return JsonResponse(
                FavorisService().get_etablishment(fid),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_user_favoris(self,request,uid):
        #   RENVOIE LES FAVORIS D'UN USER

        if request.method=='GET':
            return JsonResponse(
                FavorisService().get_user_favoris(uid),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )


########
####    FORFAIT
########
class FORFAIT:
    
    @csrf_exempt
    def save(self,request):
        #   CRE UN NOUVEL ENREGISTREMENT DE FORFAIT

        if request.method=='POST':
            return JsonResponse(
                ForfaitServive().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request, id):
        # RENVOIE LE FORFAIT AVEC L'ID AU FORMAT JSON
        
        if request.method=='GET':
            return JsonResponse(
                ForfaitServive().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )
    
    @csrf_exempt
    def list(self,request):
        #RENVOIE LA LISTE DES FORFAITS

        if request.method=='GET':
            return JsonResponse(
                ForfaitServive().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )
        
    @csrf_exempt
    def update(self,request,id):
        # MET A JOUR LE FORFAIT AVEC L'ID

        if request.method=='POST':
            return JsonResponse(
                ForfaitServive().update(request,id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def delete(self,request,id):
        # SUPPRIE LE FORFAIT AVEC L'ID

        if request.method=='DELETE':
            return JsonResponse(
                ForfaitServive().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'DELETE').format(),
            safe=True
        )
    

########
####    MEDIA
########
class MEDIA:

    @csrf_exempt
    def save(self,request):
        # CRE UN NOUVEL ENREGISTREMENT AVEC LE MEDIA

        if request.method=='POST':
            return JsonResponse(
                MediaService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )
    

    @csrf_exempt
    def show(self,request,id):
        #   RENVOIE LE MEDIA AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                MediaService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        # RENVIE UNE LISTE DE MEDIAS

        if request.method=='GET':
            return JsonResponse(
                MediaService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )
    
    @csrf_exempt
    def delete(self,request,id):
        # SUPPRIME LE MEDIA AVEC L'ID

        if request.method=='DELETE':
            return JsonResponse(
                MediaService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'DELETE').format(),
            safe=True
        )
    
    @csrf_exempt
    def get_etablishment_medias(self,request,id):
        # RENVOIE LES MEDIAS DE L'ETABLISSEMENT AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                MediaService().get_etablishment_medias(id),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )



########
####    NOTIFICATION
########
class NOTIFICATION:
    @csrf_exempt
    def save(self,request):

        if request.method=='POST':
            return JsonResponse(
                NotificationsService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )
    
    @csrf_exempt
    def show(self,request,id):
         #   RENVOIE LA NOTIFICATION AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                NotificationsService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )
    
    @csrf_exempt
    def list(self,request):
        #   RENVOIE LA LISTE DES NOTIFICATIONS

        if request.method=='GET':
            return JsonResponse(
                NotificationsService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )
    
    @csrf_exempt
    def delete(self,request,id):
        #   SUPPRIME LA NOTIFICATION AVEC L'ID

        if request.method=='DELETE':
            return  JsonResponse(
                NotificationsService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method, 'DELETE').format(),
            safe=True
        )

########
####    PAYMENT
########
class PAYMENT:

    @csrf_exempt
    def save(self,request):
        #   ENREGISTRE UN NOUVEAU PAIEMENT

        if request.method=='POST':
            return JsonResponse(
                PaymentService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )
    
    @csrf_exempt
    def show(self,request,id):
        #   RENVIE LE PAIMENT AVEC L'ID S'IL EXISTE

        if request.method=='GET':
            return JsonResponse(
                PaymentService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method, 'GET').format(),
            safe=True
        )
    
    @csrf_exempt
    def list(self,request):
        #   RENVOIE LA LISTE DES PAIMENTS

        if request.method=='GET':
            return JsonResponse(
                PaymentService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method, 'GET').format(),
            safe=True
        )
    
    @csrf_exempt
    def delete(self,request,id):
        #    SUPPRIME LES INFOS DU PAIEMENT (NE DEVRA PAS ETRE UTILISE)

        if request.method=='DELETE':
            return JsonResponse(
                PaymentService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method, 'DELETE').format(),
            safe=True
        )

    
########
####    PROMOTIONS
########
class PROMOTION:

    @csrf_exempt
    def save(self,request):
        #   ENREGISTRE UN NOUVEAU PROMOTION

        if request.method=='POST':
            return JsonResponse(
                PromotionService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE LA PROMOTION AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                PromotionService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        # RENVOIE LA LISTE DES PROMOTIONS

        if request.method=='GET':
            return JsonResponse(
                PromotionService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def delete(self,request,id):
        #   SUPPRIME LA PROMOTION AVEC L'ID

        if request.method=='DELETE':
            return JsonResponse(
                PromotionService().delete(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'DELETE').format(),
            safe=True
        )


########
####    SUBSCRIPTIONS
########
class SUBSCRIPTIONS:

    @csrf_exempt
    def save(self,request):
        # ENREGISTRE UNE NOUVELLE SUBSCRIPTION

        if request.method=='POST':
            return JsonResponse(
                SubscriptionService().save(request),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'POST').format(),
            safe=True
        )

    @csrf_exempt
    def show(self,request,id):
        # RENVOIE LA SUBSCRIPTION AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                SubscriptionService().show(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def list(self,request):
        # RENVOIE LA LISE DES SUBSCRIPTIONS

        if request.method=='GET':
            return JsonResponse(
                SubscriptionService().list(),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def get_user_subscription(self,request,uid):
        # RENVOIE LES SUBSCRIPTIONS DU USER AVEC L'ID

        if request.method=='GET':
            return JsonResponse(
                SubscriptionService().get_user_subscription(uid),
                safe=False
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )

    @csrf_exempt
    def is_paied(self,request,id):
        #  VERIFIE SI LA SUBSCRIPTION A ETE PAYEE

        if request.method=='GET':
            return JsonResponse(
                SubscriptionService().isPaied(id),
                safe=True
            )
        return JsonResponse(
            InvalidRequestMethodException(request.method,'GET').format(),
            safe=True
        )