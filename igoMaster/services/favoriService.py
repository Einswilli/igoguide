from ..models import *
from ..exceptions import *

class FavorisService:

    def get_user(self,id):
        #   RENVOIE LE USER DU FAVOIS AVEC L'ID

        try:
            return Favoris.objects.get(id=id).user.to_json()
        except:
            #   FAVORIS INTROUVABLE
            return ObjectNotFoundException('FAVORITE',id).format()

    def add(self,fid,eid):
        #   AJOUTE L'ID DE L'ETABLISSEMENT AUX FAVORIS

        try:    
            #   VERIFIER SI L'ETABLISSEMENT AVEC EID EXISTE
            e=Etablishment.objects.get(id=eid)

            #   VERIFIER SI LE FAVORIS AVEC FID EXISTE
            try:
                f=Favoris.objects.get(id=fid)
                #   ALORS ON AJOUTE L'ETABLISSEMENT
                f.add(e.id)
                return {
                    'added': True
                }
            except:
                #    FAVORIS INTROUVABLE!
                return ObjectNotFoundException('FAVORITE',fid).format()
        except:
            # ETABLISSEMET INTROUVABLE
            return ObjectNotFoundException('ETABLISHMENT',eid).format()

    def remove(self,fid,eid):
        #  SUPPRIME L'ETABLISSEMENT AVEC EID 

        try:
            # VERIFIER SI L'ETABLISSEMENT EXISTE
            e=Etablishment.objects.get(id=eid)

            #   VERIFIER SI LE FAVORIS EXISTE
            try:
                Favoris.objects.get(id=fid).remove(e.id)
                return {
                    'removed': True
                }
            except:
                # FAVORIS INTROUVABLE!
                return ObjectNotFoundException('FAVORITE',fid).format()
        except:
            # ETABLISSEMET INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',eid).format()

    def get_etablishment(self,id):
        #   RENVOIE LES ETABLISSEMENTS DU FAVORIS

        try:
            return Favoris.objects.get(id=id).get_etablishments()
        except:
            # FAVORIS INTROUVABLE
            return ObjectNotFoundException('FAVORITE',id).format()

    def get_user_favoris(self,user_id):
        # RENVOIE LES FAVORIS DU USER

        try:
            #   VERIFIER SI LE USER EXISTE
            u=User.objects.get(id=user_id)

            # VERIFIER SI LE FAVORIS
            try:
                return Favoris.objects.get(user=u.id)
            except:
                # FAVORIS INTROUVABLE!
                return ObjectNotFoundException('FAVORITE',user_id).format()
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',user_id).format()