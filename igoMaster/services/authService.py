#coding:utf-8

import random
from ..models import *
from ..exceptions import*
from igoguide.settings import *
from .emailService import EmailService

class AuthService:
    
    def login(self,request):
        # AUTHENTIFIE ET RENVOIE LE USER CORRESPONDANT 

        try:
            u=User.objects.get(Email=request.POST.get('email'))
            if u and u.Pass==request.POST.get('password'):
                request.session['user']=u.to_json()
                return u.to_json()
            #   EN CAS DE MOT DE PASSE INCORRECT!
            return InvalidAuthInformationException('PASSWORD').format()
        except:
            #   EN CAS D'E-MAIL INCORRECT!
            return InvalidAuthInformationException('EMAIL address').format()

    def pass_reset(self,request):

        e=request.POST.get('email')

        # VÉRIFIER SI L'EMAIL APPARTIENT À UN UTILISATEUR DE IGOGUIDE
        try:
            u=User.objects.get(Email__exact=e)

            #   COOL ON GENERE LE CODE DE RECUPERATION
            code=random.randrange(100000,500000)

            #   ON ENVOIE LE MAIL À UTILISATEUR
            EmailService.send_Mail(
                'RÉCUPÉRATION DE MOT DE PASSE',
                f'''<p style="">Bonjour <b>{u.FName},</b></p><br>
                Suite à votre demande de récupération de mot de passe, IGOGUIDE vous a généré un code de récupération
                de 6 (six) chiffres <span style="color:red">utilisable qu'une seule fois</span>.<br>
                code: <span style="color:deeppink">{code}</span><br><br>
                L'équipe IGOGUIDE
                ''',
                EMAIL_HOST_USER,
                [e],
                html=True
            )
            
            return {
                'sended': True,
                'message': f"L'e-mail contenant le code de récupération a été envoyé à l'adresse {e}.",
                'user':u.to_json()
            }

        except Exception as e:
            #   ON RENVOIE UN MESSAGE D'ERREUR

            msg="l'e-mail saisi n'appartient à aucun utilisateur !"
            return UnknownErrorException(str(e) + "\n Soit " + str(msg)).format()
            

    def send_pass(self,request):
        #   RENVOIE LE MOT DE PASSE PAR MAIL AU USER CORRESPONDANT

        u=User.objects.get(id=int(request.POST.get('user_id')))
        code=request.POST.get('code')
        orig_code=request.POST.get('original_code')

        # CODE D'AUTHENTIFICATON INVALIDE!
        if code!=orig_code:
            ' Le code saisi est incorrect !'
            return InvalidAuthInformationException('AUTHENTICATION CODE').format()

        #   ENVOIE DU PASSWORD
        EmailService.send_Mail(
            'RÉCUPÉRATION DE MOT DE PASSE',
            f'''{u.FName}, voici votre mot de passe:<br><h3 class="text-center text-succes" style="font-size:26">{u.Pass}</h3> .<br>
            L'équipe IGOGUIDE
            ''',
            'fiches.igoguide@gmail.com',
            [u.Email],
            html=True
        )

        return {
            'sended': True
        }