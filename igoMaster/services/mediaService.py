from models import *
from exceptions import*

class MediaService:

    def save(self,request):
        # CRE UN NOUVEL ENREGISTREMENT AVEC LE MEDIA

        m=Media.objects.create(
            name=request.POST.get('name'),
            image=request.FILES.get('image'),
            etablishment=Etablishment.objects.get(id=int(request.POST.get('etablishment_id')))
        )

        return m.to_json()

    def show(self,id):
        #   RENVOIE LE MEDIA AVEC L'ID

        try:
            return Media.objects.get(id=id).to_json()
        except:
            #   MEDIA INTROUVABLE
            return ObjectNotFoundException('MEDIA',id).format()

    def list(self):
        # RENVIE UNE LISTE DE MEDIAS

        return [
            m.to_json() for m in Media.objects.all().order_by('-id')
        ]

    def delete(self,id):
        # SUPPRIME LE MEDIA AVEC L'ID

        try:
            Media.objects.get(id=id).delete()
            return {
                'delected': True
            }
        except:
            # MEDIA INTROUVABLE!
            return ObjectNotFoundException('MEDIA',id).format()

    def get_etablishment_medias(sel,id):
        # RENVOIE LES MEDIAS DE L'ETABLISSEMENT AVEC L'ID

        try:
            #   VERIFIFER SI L'ETABLISSEMENT EXISTE
            return Etablishment.objects.get(id=id).get_medias()
        except:
            # ETABLISSEMENT INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()