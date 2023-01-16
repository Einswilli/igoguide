from models import *
from exceptions import *

class PromotionService:

    def save(self,request):
        #   ENREGISTRE UNE NOUVELLE PROMOTION
        p=Promotion.objects.create(
            duration=request.POST.get('duration'),
            text=request.POST.get('text'),
            fee=request.POST.get('fee'),
            stopDate=request.POST.get('stopDate'),
            etablishment=Etablishment.objects.get(id=int(request.POST.get('etablishment')))
        )
        return p.to_json()

    def show(self,id):
        #   RENVOIE UNE PROMOTION 

        try:
            return Promotion.objects.get(id=id).to_json()
        except:
            #   PROMOTION INTROUVABLE
            return ObjectNotFoundException('PROMOTION',id).format()

    def list(self):
        # RENVOIE LA LISTE DES PROMOTIONS

        return [
            p.to_json() for p in Promotion.objects.all().order_by('-id')
        ]

    def delete(self,id):
        #   SUPPRIME LA PROMOTION AVEC L'ID

        try:
            Promotion.objects.get(id=id).delete()
            return {
                'deleted': True
            }
        except:
            # PROMOTION INTROUVABLE!
            return ObjectNotFoundException('PROMOTION',id).format()