from models import *
from exceptions import *
from emailService import EmailService

class PaymentService:

    def save(self, request):
        #   ENREGISTRE UN NOUVEAU PAIEMENT

        p=Payment.objects.create(
            amount=request.POST.get('amount',0.0),
            status=request.POST.get('status'),
            subscription=Subscription.objects.get(id=int(request.POST.get('subscription_id')))
        )

        #   ENVOYER LE MAIL DE NOTIFICATION
        EmailService().send_Mail(
            'NOUVEAU PAIEMENT',
            f'Félicitation {p.subscription.etablishment.owner.FName}, votre paiement de {p.amount}€ a été éffectuée avec succes!',
            'leDotPy01@gmail.com',[p.subscription.etablishment.owner.Email]
            )
            
        return p.to_json()

    def show(self,id):
        #   RENVIE LE PAIMENT AVEC L'ID S'IL EXISTE

        try:
            return Payment.objects.get(id=id).to_json()
        except:
            #   PAIEMENT INTROUVABLE!
            return ObjectNotFoundException('PAYMENT',id).format()

    def list(self):
        #   RENVOIE LA LISTE DES PAIMENTS

        return [
            p.to_json() for p in Payment.objects.all()
        ]

    def delete(self,id):
        #    SUPPRIME LES INFOS DU PAIEMENT (NE DEVRA PAS ETRE UTILISE)

        try:
            Payment.objects.get(id=id).delete()
            return {
                'delected': True
            }
        except:
            # PAIEMENT INTROUVABLE!
            return ObjectNotFoundException('PAYMENT',id).format()
