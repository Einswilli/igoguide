from models import *
from exceptions import *
class UserTypeService:

    def save(self,request):
        #   CRE UN ENREGISTREMENT DE USERTYPE A PARTIR DE LA REQUETE

        u=UserType.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return u.to_json()

    def show(self,id):
        #   RENVOIE LE USERTYPE AVEC L'ID S'IL EXISTE

        try:
            return UserType.objects.get(id=id).to_json()
        except:
            #   USERTYPE INTROUVABLE
            return ObjectNotFoundException("USERTYPE", id).format()

    def get_members(self,id):
        #   RENVOIE UNE LISTE DE USER LUI APPARTENANT

        try:
            ut=UserType.objects.get(id=id)
            return ut.get_members()
        except:
            # USERTYPE INTROUVABLE!
            return ObjectNotFoundException("USERTYPE", id).format()