from models import *
from exceptions import *
from django.core.mail import send_mail

class EmailService:

    def send_register_mail(self,user,obj,emitter,recievers,msg=None,):
        if msg is None:
            msg=f'Félicitation {user} !'
        send_mail(
                message=msg,
                subject=obj,                 #  SUJET
                from_email=emitter,          #  E-MAIL EMMETEUR
                recipient_list=recievers,    #  LISTE D'E-MAILS RECEPTEURS
                fail_silently=False
            )
        return True

    def send_Mail(self,obj,msg,emitter,recievers,html=False):
        #   RetournePrend la liste des récepteurs et leur envoie le msg avec pour objet Ojb
        if html:
            send_mail(
                message=msg,
                subject=obj,                                        #  SUJET
                html_message=msg,   #  MESSAGE
                from_email=emitter,                                 #  E-MAIL EMMETEUR
                recipient_list=recievers,                           #  LISTE D'E-MAILS RECEPTEURS
                fail_silently=False
            )
        else:
            send_mail(
                message=msg,
                subject=obj,                 #  SUJET
                from_email=emitter,          #  E-MAIL EMMETEUR
                recipient_list=recievers,    #  LISTE D'E-MAILS RECEPTEURS
                fail_silently=False
            )
        return True