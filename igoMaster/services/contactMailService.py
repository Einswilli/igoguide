from ..models import *
from ..exceptions import *
from .emailService import EmailService
from igoguide import settings
class ContactMailService:

    def save(self,request):
        #   CRE UN NOUVEL ENREGISTREMENT 

        c=ContactMail.objects.create(
            subject=request.POST.get('subject'),
            message=request.POET.get('message'),
            email=request.POST.get('email'),
            fromUser=int(request.POST.get('from_user')),
            toUser=User.objects.get(id=int(request.POST.get('to_user')))
        )

        #   RECUPERER LES INFOS DE L'ETABLISSEMENT CONTACTÉ
        e=None
        try:
            e=Etablishment.objects.get(id=int(request.POST.get('etablishment_id')))

            #   INFORMATIONS EN RAPPORT AVEC LE MESSAGE
            f=f'''E-mail de Contact de IGOguide

            Nom du client : {c.get_fromUser()['FName']} {c.get_fromUser()['LName']}
            Objet du contact : {c.subject}
            E-mail du client : {c.email}
            Etablissement visité: {e.name}
            Méssage : 
                {c.message}
            '''

            #   ENVOYER UNE NOTIFICATION PAR MAIL
            EmailService().send_Mail(
                'VOUS AVEZ ÉTÉ CONTACTÉ DEPUIS IGOGUIDE!',
                f,
                settings.EMAIL_HOST_USER,
                [c.toUser.Email]
            )
            return {
                'sended':True
            }
        except Exception as ex:
            # SOIT ETABLISSEMENT INTROUVABLE SOIT ERREUR LORS DE L'ENVOIE DU MAIL
            return UnknownErrorException(str(ex)).format()

    def list(self):
        #   RENVOIE LA LISTE DES MAILS DE CONTACTS

        return [
            cm.to_json() for cm in ContactMail.objecs.all().order_by('-id')
        ] 

    def get_user_mails(self,id):
        # RENVOIE LA LISTE DES MAILS REÇUS PAR LE USER AVEC L'ID

        try:
            # VERIFIER SI LE USER EXISTE
            u=User.objects.get(id=id)
            return [
                cm.to_json() for cm in ContactMail.objects.filter(user=u.id).order_by('-id')
            ]
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def get_user_unread_mails(self,id):
        # RENVOIE LA LISTE DES MAILS NON LUS REÇUS PAR LE USER AVEC L'ID

        try:
            # VERIFIER SI LE USER EXISTE
            u=User.objects.get(id=id)
            return [
                cm.to_json() for cm in ContactMail.objects.filter(user=u.id,isOpened=False).order_by('-id')
            ]
        except:
            # USER INTROUVABLE!
            return ObjectNotFoundException('USER',id).format()

    def show(self,id):
        #   RENVOIE LE MAIL AU FORMAT JSON

        try:
            # VERIFIER SI LE MAIL EXISTE
            return ContactMail.objects.get(id=id).to_json()
        except:
            # MAIL INTROUVABLE!
            return ObjectNotFoundException('MAIL',id).format()

    def delete(self,id):
        # SUPPRIME LE MAIL AVEC L'ID S'IL EXISTE

        try:
            # VERIFIER SI LE MAIL EXISTE
            ContactMail.objects.get(id=id).delete()
            return {
                'delected': True
            }
        except:
            #   MAIL INTROUVABLE!
            return ObjectNotFoundException('MAIL',id).format()