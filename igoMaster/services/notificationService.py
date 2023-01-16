from models import*
from exceptions import*
from .emailService import EmailService

class NotificationsService:

    def save(self,request):

        try:
            n=Notification.objects.create(
                message=request.POST.get('message',''),
                fromUser=request.POST.get('from_user_id','{}'),
                toUser=User.objects.get(id=int(request.POST.get('to_user_id')))
            )

            #   ENVOYER LLA NOTIFICATION PAR MAIL
            EmailService().send_Mail(
                'NOUVELLE NOTIFICATION!',
                n.message,
                'leDotPy01@gmail.com',
                [n.toUser.Email]
            )

            return n.to_json()
        except Exception as e:
            return {
                'Status': 'failed',
                'Error': {
                    'name':'UnknownErrorException',
                    'message': str(e),
                    'code':5
                }
            }

    def show(self,id):
        #   RENVOIE LA NOTIFICATION AVEC L'ID

        try:
            return Notification.objects.get(id=id).to_json()
        except:
            #   NOTIFICATION INTROUVABLE
            return ObjectNotFoundException('NOTIFICATION',id).format()

    def list(self):
        #   RENVOIE LA LISTE DES NOTIFICATIONS

        return [
            n.to_json() for n in Notification.objects.all()
        ]

    def delete(self,id):
        #   SUPPRIME LA NOTIFICATION AVEC L'ID

        try:
            Notification.objects.get(id=id).delete()
        except:
            # NOTIFICATION INTROUVABLE!
            return ObjectNotFoundException('NOTIFICATION',id).format()