from ..models import *
from ..exceptions import *
from .emailService import EmailService

class UserService(models.Model):

    def save(self,request):
        #   CRE UN NOUVEL ENREGISTREMENT DE USER A PARTIR DE LA REQUETE

        type=2 if request.POST.get('type')=='particular' else 1

        u=User.objects.create(
            LName=request.POST.get('last_name'),
            FName=request.POST.get('first_name'),
            Email=request.POST.get('email'),
            Phone=request.POST.get('phone'),
            Pass=request.POST.get('password'),
            Type=UserType.objects.get(id=type),
            # Photo=request.FILES.get('photo')
        )

        #   ON CRE LE FAVORIS SI LE TYPE EST 1 "PARTICULIER"

        if type==2:
            Favoris.objects.create(
                user=u
            )

        #   ENVOYER UN EMAIL D'INSCRIPTION
        EmailService().send_register_mail(
            u.FName,'Inscription réussi','leDotPy01@gmail.com',[u.Email]
        )
        
        return u.to_json()

    def update(self,request,id):
        #    MET A JOUR UN UTILISATEUR

        try:
            u=User.objects.get(id=id)
            u.Lname = request.POST.get('last_name')
            u.Fname = request.POST.get('first_name')
            u.Email = request.POST.get('email')
            u.Phone = request.POST.get('phone')
            u.save()
            return u.to_json()
        except:
            #   USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def show(self,id):
        #   RETOURNE LE USER AVEC L'ID

        try:
            return User.objects.get(id=id).to_json()
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def delete(self,id):
        # SUPPRIME LE USER AVEC L'ID

        try:
            User.objects.get(id=id).delete()
            return {
                'deleted': True
            }
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def list(self):
        # RENVOIE LA LISTE 

        return[
            x.to_json() for x in User.objects.all().order_by('-id')
        ]

    def get_etablissements(self,id):
        # RETOURNE LA LISTE DES ETABLISSEMENTS DU USER AVEC L'ID S'IL EST PROFESSIONNEL

        try:
            u=User.objects.get(id=id)
            if u.type.id==1: #  SEULEMENT SI LE USER EST UN PRO!
                return u.get_etablissements()
            return UncompatibleUserTypeException(
                'PROFESSIONAL','PARTICULAR'
            ).format()
        except:
            #   USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def get_notifications(self,id):
        # RETOURNE LA LISTE DES NOTIFICATIONS DU USER AVEC L'ID

        try:
            u=User.objects.get(id=id)
            if u.type.id==1: # SEULEMENT SI LE USER EST PRO!
                return u.get_notifications()
            return UncompatibleUserTypeException(
                'PROFESSIONAL','PARTICULAR'
            ).format()
        except:
            #   USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def get_mails(self,id):
        #   RETOURNE LA LISTE DES MAILS DE CONTACTS DU USER AVEC L'ID

        try:
            u=User.objects.get(id=id)
            if u.type.id==1: # SEULEMENT SI LE USER EST PRO!
                return u.get_mails()
            return UncompatibleUserTypeException(
                'PROFESSIONAL','PARTICULAR'
            )
        except: 
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def add_favoris(self,uid,eid):
        #   AJOUTE L'ETABLISSEMENT AVEC L'ID AUX FAVORIS DU USER S'IL EXISTE
        try:
            return User.objects.get(id=uid).add_favoris(eid)
        except:
            return ObjectNotFoundException('USER',uid).format()

    def remove_favoris(self,uid,eid):
        #   SUPPRIME L'ETABLISSEMENT AVEC L'ID DES FAVORIS DU USER S'IL EXISTE
        try:
            return User.objects.get(id=uid).remove_favoris(eid)
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',uid).format()

    def get_favoris(self,uid):
        #   RENVOIE LES FAVORIS DU USER AVEC L'ID
        try:
            return User.objects.get(id=uid).get_favoris()
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',uid).format()