from models import *
from exceptions import *

class BannerService:

    def save(self,request):
        # CRE UN NOUVEL ENREGISTREMENT DE BANIERE

        b=Banner.objects.create(
            name=request.POST.get('name','banner_name'),
            image=request.FILES.get('image')
        )

        return b.to_json()

    def show(self,id):
        # RENVOIE LE BANNER AVEC L'ID

        try:
            return Banner.objects.get(id=id).to_json()
        except:
            # BANNER INTROUVABLE!
            return ObjectNotFoundException('BANNER',id).format()

    def delete(self,id):
        # SUPPPRIME LE BANNER AVEC L'ID

        try:
            Banner.objects.get(id=id).delete()
            return {
                'delected': True
            }
        except:
            # BANNER INTROUVABLE!
            return ObjectNotFoundException('BANNER',id).format()

    def list(self):
        # RENVOIE LA LISTE DES BANNERS

        return [
            b.to_json() for b in Banner.objects.all().order_by('-id')
        ]