from models import *
from exceptions import*
from .emailService import EmailService

class SubscriptionService:

    def save(self,request):
        # CRE UN NOUVEL ENREGISTREMENT 
        
        s=Subscription.objects.create(
            activeDuration=int(request.POST.get('activeDuration')),
            fee=float(request.POST.get('fee')),
            stopDate=request.POST.get('stopDate'),
            etablishment=Etablishment.objects.filter(id=int(request.POST.get('etablishment_id')))
        )

        return s.to_json()

    def show(self,id):
        # RENVOIE LA SUBSCRIPTION AVEC L'ID SI ELLE EXISTE
        
        try:
            return Subscription.objects.get(id=id).to_json()
        except:
            # SUBSCRIPTION INTROUVABLE
            return ObjectNotFoundException('SUBSCRIPTION',id).format()

    def list(self):
        # RENVOIE LA LISTE DES SUBSCRIPTIONS
        return [
            s.to_json() for s in Subscription.objects.all().order_by('-id')
        ]

    def get_user_subscription(self,id):
        # RENVOIE LA LISTE DES SUBSCRIPTIONS DU USER
        try:
            #   VERIFIER SI LE USER EXISTE
            u=User.objects.get(id=id)
            return [
                s.to_json() for s in Subscription.objects.filter(etablishment__owner=u.id).order_by('-id')
            ]
        except:
            # SUBSCRIPTION INTROUVABLE!
            return ObjectNotFoundException('SUBSCRIPTION',id).format()

    def isPaied(self,id):
        # VERIFIE SI LA SUBSCRIPTION A ETE PAYEE
        
        try:
            return {
                'okay':Subscription.objects.get(id=id).isPaied()
            }
        except:
            return ObjectNotFoundException('SUBSCRIPTION',id).format()