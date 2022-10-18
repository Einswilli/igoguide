from email import message
import re
import time
import random
import timeago
from .models import *
import simplejson as Json
from django import template
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# Create your views here.

#######
###     ACCUEIL
#######

def home(request):
    # Retourne la page d'accueil
    # fillcat()
    return render(request,'accueil.html')

def faq(request):
    return render(request,'dashboard/pages/faq.html')

def cgv(request):
    return render(request,'dashboard/pages/cgv.html')

def cgu(request):
    return render(request,'dashboard/pages/cgu.html')

def cgu_footer(request):
    return render(request, 'cgu_footer.html')

def faq_footer(request):
    return render(request, 'faq_footer.html')

def fillcat():
    et=None
    with open('igoMaster/data/EtablishmentSubTypes.json','r')as f:
        et=Json.loads(f.read())['EtablishmentSubTypes']
    for e in et:
        EtablishmentSubType.objects.create(
            name=e['name'],
            description=e['description'],
            type=EtablishmentType.objects.get(id=e['etablishment_type_id'])
        )

#######
###     AUTHENTIFICATION ET ENREGISTREMENT PARTICULIERS
#######

#######     PARTICULIERS    ###

def pass_reset(request):
    e=request.POST.get('email')
    #Vérifier si l'email saisi appartient à un utilisateur 
    if e not in ('',None):
        try:
            u=User.objects.get(Email__exact=e)

            #On génère le code de récupération
            code=random.randrange(100000,500000)
            #Alors on envoie le mail à l'adresse!
            send_Mail(
            'RÉCUPÉRATION DE MOT DE PASSE',
            f'''<p style="">Bonjour <b>{u.FName},</b></p><br>
            Suite à votre demande de récupération de mot de passe, IGOGUIDE vous a généré un code de récupération
            de 6 (six) chiffres <span style="color:red">utilisable qu'une seule fois</span>.<br>
            code: <span style="color:deeppink">{code}</span><br><br>
            L'équipe IGOGUIDE
            ''',
            'fiches.igoguide@gmail.com',
            [e],
            html=True
            )
            msg=f"L'e-mail contenant le code de récupération a été envoyé à l'adresse {e}."
        except Exception as e:
            print(e)
            #   On renvoie un méssage d'erreur!
            #   Avec un code Null
            code=None
            u=None
            msg="Erreur: l'e-mail saisi n'appartient à aucun utilisateur !"

        return render(request,'auth/passReset.html',{'msg':msg,'code':code,'user':u})
    # msg="Erreur: Assurez vous d'avoir bien rempli le champ!"
    # return render(request,'auth/passReset.html',{'msg':msg})

def send_pass(request):
    u=User.objects.get(id=int(request.POST.get('userid')))
    code=request.POST.get('code')
    orig_code=request.POST.get('orig_code')

    if code!=orig_code:
        msg=' Le code saisi est incorrect !'
        return render(request,'auth/passReset.html',{'msg':msg,'code':orig_code,'user':u})

    send_Mail(
        'RÉCUPÉRATION DE MOT DE PASSE',
        f'''{u.FName}, voici votre mot de passe:<br><h3 class="text-center text-succes" style="font-size:26">{u.Pass}</h3> .<br>
        L'équipe IGOGUIDE
        ''',
        'fiches.igoguide@gmail.com',
        [u.Email],
        html=True
    )

    if u.Type.id==2:
        return render(request,'auth/particular/login.html')
    return render(request,'auth/professional/login.html')

@csrf_exempt
def particular_auth(request):
    #   Retourne la page de connexion pour les particuliers
    return render(request,'auth/particular/login.html')

def particular_login(request):
    #   Retourne la page l'accueil avec l'utilisateur connecté s'il existe
    #   sinon renvoie un message d'erreur 

    email=request.POST.get('email')
    paswd=request.POST.get('password')

    try:
        #Essayer de recuperer l' user avec l'Email==email!
        u=User.objects.get(Email__exact=email,Type__id=2)
        if u!=None:
            #Alors on vérifie le pass
            if u.Pass==paswd:
                user={
                    'id':u.id,
                    'lname':u.LName,
                    'fname':u.FName,
                    'email':u.Email,
                    'telephone':u.Phone,
                    'favorites':[e.etablishment.id for e in Favoris.objects.filter(user=u.id)]
                }
                request.session['client']=user
                return render(request,'accueil.html',{'client':user})
            else:
                msg='mot de passe invalide!'
                return render(request,'auth/particular/login.html',{'msg':msg})
    except Exception as e:
        print(e)
        msg='E-mail invalide!'
        return render(request,'auth/particular/login.html',{'msg':msg})

def new_particular(request):
    #   Retourne la page de REGISTER des particuliers
    return render(request,'auth/particular/register.html')

def particular_register(request):
    # Renvoie l'utilisateur en mode connecté sur la page d'acceul apres l'avoir créé
    # Sinon un message d'erreur
    
    if request.POST.get('pass')!=request.POST.get('pass_confirm'):
        msg='Les champs de mot de passe doivent être identique!'
        return render(request,'auth/particular/register.html',{'msg':msg})
    if request.FILES.get('photo')==None:
        msg='Veuillez Choisir une photo'
        return render(request,'auth/professional/register.html',{'msg':msg})
    msg=None
    if validate(request):
        User.objects.create(
            LName=request.POST.get('lname'),
            FName=request.POST.get('fname'),
            Email=request.POST.get('email'),
            Phone=request.POST.get('phone'),
            Pass=request.POST.get('pass'),
            Type=UserType.objects.get(id=2),
            Photo=request.FILES.get('photo')
        )
        msg='Compte Créé avec succes! Authentifiez vous.'
        return render(request,'auth/particular/login.html')
    else:
        msg='Formulaire invalide!'
        return render(request,'auth/particular/register.html',{'msg':msg})

def get_particular_profile(request,id):
    if request.method=='GET':
        u=User.objects.get(id=id)
        f=Favoris.objects.filter(user=u.id)
        favs=[{
            'id':e.etablishment.id,
            'name':e.etablishment.name,
            'address':e.etablishment.address,
            'presentation':e.etablishment.presentation,
            'longitude':e.etablishment.longitude,
            'latitude':e.etablishment.latitude,
            'city':e.etablishment.city,
            'tags':e.etablishment.tags,
            'postal':e.etablishment.postal,
            'contact':Contact.objects.get(etablishment=e.etablishment.id),
            'reseaux':Social.objects.get(etablishment=e.etablishment.id),
            'subType':e.etablishment.subType.name,
            'subTypeText':e.etablishment.subType.description,
            'subtypeid':e.etablishment.subType.id,
            'type':e.etablishment.subType.type.name,
            'owner':e.etablishment.owner,
            'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.etablishment.id)],
            'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.etablishment.subType.id)]
        } for e in f]
        return render(request,'particular_profile.html',{'client':u,'etablissements':favs})

#######     PROFESSIONNELS    ###

def professional_auth(request):
    # Retourne la page de connexion pour les professionnels
    return render(request,'auth/professional/login.html')

def professional_login(request):
    #   Retourne l'utilisateur en mode connecté sur  le dashboard professionnel
    #   Sinon un méssage d'erreur

    #Récuperation des infos depuis le POST
    email=request.POST.get('email')
    paswd=request.POST.get('pass')

    try:
        #Essayer de recuperer l' user avec l'Email==email!
        u=User.objects.get(Email__exact=email,Type=1)
        if u!=None:
            #Alors on vérifie le pass
            if u.Pass==paswd:
                request.session['user']=u
                return render(request,'dashboard/index.html',{'user':u})
            else:
                msg='Erreur: mot de passe invalide!'
                return render(request,'auth/professional/login.html',{'msg':msg})
    except Exception as e:
        print('ERREUR',e)
        msg='Erreur: E-mail invalide!'
        return render(request,'auth/professional/login.html',{'msg':msg})

def new_professional(request):
    #   Retourne la page de REGISTER des professionnels
    return render(request,'auth/professional/register.html')

def professional_register(request):
    #   Retourne l'utilisateur en mode connecté sur le dashboard professionnel
    #   Apres l'avoir créé sinon un message d'erreur

    #   Si Password != ppassword_confirm 
    if request.POST.get('pass')!=request.POST.get('pass_confirm'):
        msg='Les champs de mot de passe doivent être identique!'
        return render(request,'auth/professional/register.html',{'msg':msg})
    if request.FILES.get('photo')==None:
        msg='Veuillez Choisir une photo'
        return render(request,'auth/professional/register.html',{'msg':msg})
    msg=None
    if validate(request):
        User.objects.create(
            LName=request.POST.get('lname'),
            FName=request.POST.get('fname'),
            Email=request.POST.get('email'),
            Phone=request.POST.get('phone'),
            Pass=request.POST.get('pass'),
            Type=UserType.objects.get(id=1),
            Photo=request.FILES.get('photo')
        )
        msg='Compte Créé avec succes! Authentifiez vous.'
        return render(request,'auth/professional/login.html',{'msg':msg})
    else:
        msg='Formulaire invalide!'
        return render(request,'auth/professional/register.html',{'msg':msg})

def get_user_profile(request,id):
    u=User.objects.get(id=id)
    return render(request,'dashboard/pages/profile.html',{'user':u})

######
###     CATEGORIES
######

def get_categorieX(request,id):
    # Renvoie sur la page de la catégorie id

    et=EtablishmentType.objects.get(id=id)          #   POUR AVOIR LA CATEGORIE EN QUESTION
    es=EtablishmentSubType.objects.filter(type=id)  #   POUR AVOIRS SES SOUS-CATEGORIES

    return render(request,'categorie.html',{'EtablishmentType':et,'EtablishmentSubTypes':es})


######
###     ETABLISSEMENTS
######

def new_etablishment(request):
    #   Renvoie la page de création des établissements
    return render(request,'dashboard/etablissements/new.html')

def get_etablishment_details(request,id):
    # Renvoie la page de detail de l'établissement X
    e=Etablishment.objects.get(id=id)
    es={
        'id':e.id,
        'name':e.name,
        'address':e.address,
        'presentation':e.presentation,
        'longitude':e.longitude,
        'latitude':e.latitude,
        'city':e.city,
        'tags':e.tags,
        'postal':e.postal,
        'contact':Contact.objects.get(etablishment=e.id),
        'reseaux':Social.objects.get(etablishment=e.id),
        'subType':e.subType.name,
        'subTypeText':e.subType.description,
        'subtypeid':e.subType.id,
        'type':e.subType.type.name,
        'owner':e.owner,
        #'other':Json.loads(OTHER.objects.get(etablishment=e.id).content) or '',
        'typeColor':e.subType.type.color,
        'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
        'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
    }
    return render(request,'etablissements/detail.html',{'e':es})

def save_etablishment(request):
    #   On crée ici l'établissement
    if request.method=='POST':

        other_ctx={}
        #Récuperer les infos
        name=request.POST.get('name')
        pres=request.POST.get('presentation')
        adr=request.POST.get('searchTextField')
        tags=request.POST.get('tags')
        lng=request.POST.get('longitude')
        lat=request.POST.get('latitude')
        postal=request.POST.get('code_postal')
        subcat=request.POST.get('sous_cat')
        cat=request.POST.get('categorie')
        user=request.POST.get('userfield')

        ######INFOS CONTACT
        tel=request.POST.get('telephone')
        email=request.POST.get('email')
        website=request.POST.get('website')

        ######INFOS VILLE
        city=request.POST.get('ville')
        reg=request.POST.get('region')
        dept=request.POST.get('departement')
        country=request.POST.get('pays')

        c=None
        try:
            c=City.objects.get(name__icontains=city)
        except:
            # créer la ville si elle n'existe pas!
            c=City.objects.create(
                name=city,
                region=reg,
                department=dept,
                country=country
            )

        ######INFOS RÉSEAUX SOSCIAUX
        fb=request.POST.get('facebook')
        insta=request.POST.get('instagram')

        ######MEDIAS
        img=request.FILES.get('image')

        if int(cat)==1:     # Hébergement
            #Alors on save une activité
            other_ctx={
                'Tarif à partir de':request.POST.get('heb_tarif'),
                "Capacité d'accueil":request.POST.get('capaciteAccueil'),
                'Âge minimum':request.POST.get('heb_min_age'),
                'Nombre de couchages':request.POST.get('heb_ncouchage'),
                'Piscine':request.POST.get('picine'),
                'Bain à remous':request.POST.get('bain_remous'),
                'Sauna':request.POST.get('sauna'),
                'Cuisine':request.POST.get('cuisine'),
                'Salles de bains et wc':request.POST.get('bain_wc'),
                'Accès internet':request.POST.get('ac_internet'),
                'Ménage inclus':request.POST.get('menage'),
                'Drap et linges inclus':request.POST.get('drap_linge'),
                'Animaux':request.POST.get('animaux'),
                'Enfants':request.POST.get('enfants'),
                'Petits déjeuners':request.POST.get('ptidej'),
                'Lits simples':request.POST.get('lits_simples'),
                'Lits doubles':request.POST.get('lits_db'),
                "lits d'appoint":request.POST.get('lits_appoint'),
                'Lits pour bébés':request.POST.get('lits_bb'),
                'Lit canapé':request.POST.get('lit_canape'),
                'Lit supperposés':request.POST.get('lit_supp'),
                'Accessible aux handicapés':request.POST.get('handicap'),
                'Possibilité de manger sur place':request.POST.get('m_sur_place'),
            }

        elif int(cat)==2:       # Bars
            other_ctx={
                "Heure d'ouverture":request.POST.get('bar_h_ouverture'),
                "Heure de fermeture":request.POST.get('bar_h_fermeture'),
                "Tarif à partir de":request.POST.get('bar_tarif'),
                "Accessible aux handicapés":request.POST.get('bar_handicap')
            }
        elif int(cat)==3:       # Restaurants
            other_ctx={
                "Jours non ouverts":request.POST.get('resto_jn_ouverts'),
                "Heure d'ouverture":request.POST.get('resto_h_ouverture'),
                "Heure de fermeture":request.POST.get('resto_h_fermeture'),
                "Familles avec enfants":request.POST.get('cfenfant'),
                "Groupe d'amis":request.POST.get('cgroupe'),
                "Repas sur place":request.POST.get('repas_sur_place'),
                "Repas emportés":request.POST.get('repas_emporte'),
                "Livraisons":request.POST.get('livraison'),
                "Accessible aux handicapés":request.POST.get('resto_handicap')
            }
        elif int(cat)==4:
            pass
        elif int(cat)==5:
            pass
        elif int(cat)==6:
            pass

        if user==None:
            msg="Une erreur s'est produite!"
            return render(request,'dashboard/etablissements/new.html',{'msg':msg})

        #creer l'etablissement
        e=Etablishment.objects.create(
            name=name,
            presentation=pres,
            address=adr,
            tags=tags,
            longitude=lng,
            latitude=lat,
            postal=postal,
            city=c,
            subType=EtablishmentSubType.objects.get(id=int(subcat)),
            owner=User.objects.get(id=int(user))
        )
        if e:
            #   On rajoute les infos supps
            OTHER.objects.create(
                content=Json.dumps(other_ctx,indent=4),
                etablishment=e
            )
            #   On cré le contact
            Contact.objects.create(
                telephone=tel,
                email=email,
                website=website,
                etablishment=e
            )
            #   On cré les réseaux sociaux
            Social.objects.create(
                facebookName=fb,
                instagramName=insta,
                etablishment=e
            )
            #   On cré le premier média
            Media.objects.create(
                name=name,
                image=img,
                etablishment=e
            )
            #   On cré l'abonnement
            Subscription.objects.create(
                stopDate=date.today() + relativedelta(months=2),
                etablishment=e
            )
            msg='SUCCES!'
        else:msg='ERREUR!'
        return render(request,'dashboard/etablissements/new.html',{'msg':msg})

def edit_etablishment(request,id):
    if request.method=='POST':
        name=request.POST.get('name')
        pres=request.POST.get('presentation')
        adr=request.POST.get('searchTextField')
        tags=request.POST.get('tags')
        lng=request.POST.get('longitude')
        lat=request.POST.get('latitude')
        postal=request.POST.get('code_postal')
        subcat=request.POST.get('souscategorie')
        tel=request.POST.get('telephone')
        email=request.POST.get('email')
        website=request.POST.get('website')
        city=request.POST.get('ville')
        reg=request.POST.get('region')
        dept=request.POST.get('departement')
        country=request.POST.get('pays')
        fb=request.POST.get('facebook')
        insta=request.POST.get('instagram')
        c=None
        try:
            c=City.objects.get(name__icontains=city)
        except:
            # créer la ville si elle n'existe pas!
            c=City.objects.create(
                name=city,
                region=reg,
                department=dept,
                country=country
            )

        ###### Etablishment
        e=Etablishment.objects.get(id=id)
        e.name=name
        e.presentation=pres
        e.address=adr
        e.tags=tags
        e.longitude=lng
        e.latitude=lat
        e.postal=postal
        e.subType=EtablishmentSubType.objects.get(id=int(subcat))
        e.city=c
        e.save()

        ###### Contact
        cn=Contact.objects.get(
            etablishment=e.id
        )
        cn.telephone=tel
        cn.email=email
        cn.website=website
        cn.save()

        ###### Reseaux
        s=Social.objects.get(
            etablishment=e.id
        )
        s.facebookName=fb
        s.instagramName=insta
        s.save()

        return list_user_etablishments(request,e.owner.id)
        
        

def delete_etablishment(request,id):
    e=Etablishment.objects.get(id=id)
    owner=e.owner.id
    if e:
        # Etablishment.objects.delete(id=id)
        e.delete()
        return list_user_etablishments(request,owner)

def get_user_etablishments(request,id):
    
    if request.method=='GET':
        etablissements=[{
            'id':e.id,
            'name':e.name,
            # 'address':e.address,
            # 'presentation':e.presentation,
            # 'longitude':e.longitude,
            # 'latitude':e.latitude,
            # 'city':e.city,
            # 'tags':e.tags,
            # 'postal':e.postal,
            # 'contact':Contact.objects.get(etablishment=e.id),
            # 'reseaux':Social.objects.get(etablishment=e.id),
            # 'subType':e.subType.name,
            # 'subTypeText':e.subType.description,
            # 'subtypeid':e.subType.id,
            # 'type':e.subType.type.name,
            # 'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
            # 'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
        }for e in Etablishment.objects.filter(owner=id)]
        return JsonResponse(etablissements,safe=False)

def list_user_etablishments(request,id):
    # Liste les etablissements appartenant a un professionnel X
    etablissements=[{
        'id':e.id,
        'name':e.name,
        'address':e.address,
        'presentation':e.presentation,
        'longitude':e.longitude,
        'latitude':e.latitude,
        'city':e.city,
        'tags':e.tags,
        'postal':e.postal,
        'contact':Contact.objects.get(etablishment=e.id),
        'reseaux':Social.objects.get(etablishment=e.id),
        'subType':e.subType.name,
        'subTypeText':e.subType.description,
        'subtypeid':e.subType.id,
        'type':e.subType.type.name,
        'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
        'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
    }for e in Etablishment.objects.filter(owner=id)]
    return render(request,'dashboard/etablissements/list.html',{'etablissements':etablissements})

def get_dept_etablishments(request,id):
    
    dept_name=get_department_by_id(id)['name'].lower()
    if dept_name not in ('',None):
        
        l=[{
            'id':e.id,
            'name':e.name,
            'address':e.address,
            'presentation':e.presentation,
            'longitude':e.longitude,
            'latitude':e.latitude,
            'city':e.city,
            'tags':e.tags,
            'postal':e.postal,
            'contact':Contact.objects.get(etablishment=e.id),
            'reseaux':Social.objects.get(etablishment=e.id),
            'subType':e.subType.name,
            'subTypeText':e.subType.description,
            'subtypeid':e.subType.id,
            'type':e.subType.type.name,
            'owner':e.owner,
            'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
            'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
        }for e in Etablishment.objects.filter(city__name__icontains=dept_name)]
        return render(request,'etablissements/liste.html',{'etablissements':l,'text':dept_name})

def get_reg_etablishments(request,reg):
    if reg not in ('',None):
        
        l=[{
            'id':e.id,
            'name':e.name,
            'address':e.address,
            'presentation':e.presentation,
            'longitude':e.longitude,
            'latitude':e.latitude,
            'city':e.city,
            'tags':e.tags,
            'postal':e.postal,
            'contact':Contact.objects.get(etablishment=e.id),
            'reseaux':Social.objects.get(etablishment=e.id),
            'subType':e.subType.name,
            'subTypeText':e.subType.description,
            'subtypeid':e.subType.id,
            'type':e.subType.type.name,
            'owner':e.owner,
            'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
            'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
        }for e in Etablishment.objects.filter(city__region__icontains=reg)]
        return render(request,'etablissements/liste.html',{'etablissements':l,'text':reg})

def search_etablishment(request):
    if request.method=='POST':
        mc=request.POST.get('mc')
        loc=request.POST.get('loc')
        user=None
        if request.POST.get('client')not in ('',None):
            u=User.objects.get(id=int(request.POST.get('client')))
            user={
                'id':u.id,
                'lname':u.LName,
                'fname':u.FName,
                'email':u.Email,
                'telephone':u.Phone,
                'favorites':[e.etablishment.id for e in Favoris.objects.filter(user=u.id)]
            }


        text=''
        if mc and loc:
            text=f'{mc} dans {loc}'
        elif mc and not loc:
            text=mc
        else:text=loc
        #Alors on recherche le mot clé dans la localité
        etablissements=[{
            'id':e.id,
            'name':e.name,
            'address':e.address,
            'presentation':e.presentation,
            'longitude':e.longitude,
            'latitude':e.latitude,
            'city':e.city,
            'tags':e.tags,
            'postal':e.postal,
            'contact':Contact.objects.get(etablishment=e.id),
            'reseaux':Social.objects.get(etablishment=e.id),
            'subType':e.subType.name,
            'subTypeText':e.subType.description,
            'subtypeid':e.subType.id,
            'type':e.subType.type.name,
            'owner':e.owner,
            'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
            'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
        }for e in Etablishment.objects.all()]
        l=[]
        for i in etablissements:
            if mc and loc:
                if x_in_city(loc,i['city']) or loc.lower() in i['address'] and x_in_etab(mc,i):
                    l.append(i) 
            elif mc and not loc:
                if x_in_etab(mc,i):
                    l.append(i)
            elif not mc and loc:
                if x_in_city(loc,i['city']) or loc.lower() in i['address']:
                    l.append(i)
            else:pass
        random.shuffle(l)
        return render(request,'etablissements/liste.html',{'etablissements':l,'text':text,'client':user})
    return JsonResponse('NOT FOUND',safe=False)


def x_in_city(x,city):
    # rechercher par localisation
    if not x or x=='': return False
    atrs=[city.name,city.region,city.country,city.department]
    for i in atrs:
        if x.lower() in i.lower():
            return True 
    return False 

def x_in_etab(x,etab):
    # Rechercher par mots clés
    if not x or x=='': return False
    atrs=[
        etab['presentation'],etab['tags'],etab['name'],
        etab['address'],etab['subType'],
        etab['subTypeText'],
        etab['type']
    ]
    for i in atrs:
        if x.lower() in i.lower():
            return True 
    return False 

def list_subtypeX_etablishment(request,id):
    
    etablissements=[{
        'id':e.id,
        'name':e.name,
        'address':e.address,
        'presentation':e.presentation,
        'longitude':e.longitude,
        'latitude':e.latitude,
        'city':e.city,
        'tags':e.tags,
        'postal':e.postal,
        'contact':Contact.objects.get(etablishment=e.id),
        'reseaux':Social.objects.get(etablishment=e.id),
        'subType':e.subType.name,
        'subTypeText':e.subType.description,
        'subtypeid':e.subType.id,
        'type':e.subType.type.name,
        'owner':e.owner,
        'images':[{'url':i.image.url,'name':i.name} for i in Media.objects.filter(etablishment=e.id)],
        'type_subtypes':[{'name':i.name,'id':i.id,'desc':i.description} for i in EtablishmentSubType.objects.filter(type=e.subType.id)],
    }for e in Etablishment.objects.filter(subType=id)]
    return render(request,'etablissements/liste.html',{'etablissements':etablissements,'text':EtablishmentSubType.objects.get(id=id).name})


######
###     ABONNEMENTS
######

def new_subscription(request):
    #   Renvoie la page de création des abonnements
    return render(request,'dashboard/abonnements/new.html')

def save_subscription(request):
    #   Enregistre l'abonnement depuis le POST
    if request.method=='POST':
        print(request.POST)
        Subscription.objects.create(
            activeDuration=request.POST.get('mois'),
            fee=float(request.POST.get('total')[:-2]),
            stopDate=date.today()+relativedelta(months=int(request.POST.get('mois'))),
            etablishment=Etablishment.objects.get(id=int(request.POST.get('etablissement')))
        )
        msg='SUCCES!'
    else:
        msg='ERREUR METHODE NON AUTORISÉE'
    return render(request,'dashboard/abonnements/new.html',{'msg':msg})

def list_user_subscriptions(request,id):
    # liste les abonnements de l'user
    s=Subscription.objects.filter(etablishment__owner=id)
    return render(request,'dashboard/abonnements/list.html',{'subscriptions':s})

def new_payment(request,id):
    pass

def list_user_payments(request,id):
    # liste les paiements de l'user
    return render(request,'dashboard/abonnements/payments.html')


######
###     UTILISATEURS
######


def get_professional_user(request,id):
    #Renvoie le compte du professionnel avec l'id=id
    if request.method=='GET':
        user=User.objects.get(id=id)
        u={
            'id':user.id,
            'lname':user.LName,
            'fname':user.FName,
            'type':user.Type.name,
            'image':user.Photo.url
        }
        return JsonResponse(u,safe=True)

def get_particular_user(request,id):
    if request.method=='GET':
        print('contact!')
        u=User.objects.get(id=id)
        user={
            'id':u.id,
            'lname':u.LName,
            'fname':u.FName,
            'email':u.Email,
            'telephone':u.Phone,
            'favorites':[e.etablishment.id for e in Favoris.objects.filter(user=u.id)]
        }
        return JsonResponse(user,safe=True)
    return JsonResponse('METHOD NOT ALLOWED',safe=True)

def change_user_pass(request,id):
    pass

def update_user(request,id):
    data = User.objects.get(id = id)
    
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(data.Photo) > 0:
                os.remove(data.Photo.path)
            data.Photo = request.FILES['Photo'] 
        data.lname = request.POST.get('lname')
        data.fname = request.POST.get('fname')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.save()
        #message.success(request, 'Modification enrégistrer')
        return redirect(request, 'dashboard/pages/profile.html')

# Modification du profile du professionel
def update_professional_user(request,id):
    get_professional_user(request,id)


######
###     MAILS
######

def get_user_mails(request,id):
    c=ContactMail.objects.filter(toUser=id).order_by('-createdAt','isOpened')
    u=ContactMail.objects.filter(toUser=id,isOpened=False).count()
    l=[{
        'id':m.id,
        'subject':m.subject,
        'email':m.email,
        'massage':m.message,
        'isOpened':m.isOpened,
        'fromUser':User.objects.get(id=m.fromUser),
        'createdAt':m.createdAt,
    } for m in c]
    return render(request,'dashboard/messages/emails.html',{'emails':l,'unreads':u})

def get_mailX(request,id):
    m=ContactMail.objects.get(id=id)
    u=User.objects.get(id=m.fromUser)
    m.isOpened=True
    m.save()
    c={
        'id':m.id,
        'subject':m.subject,
        'email':m.email,
        'message':m.message,
        'isOpened':m.isOpened,
        'fromUser':{
            'id':u.id,
            'LName':u.LName,
            'FName':u.FName,
            'image':u.Photo.url,
            'Email':u.Email,
            'Telephone':u.Phone
            },
        'createdAt':timeago.format(
            m.createdAt,datetime.now() + timedelta(seconds = 60 * 3.4),
            'fr'
            ) #(datetime.today().date() - m.createdAt),
    }
    return JsonResponse(c,safe=True)

def get_user_unread_mails_count(request,id):
    u=ContactMail.objects.filter(toUser=id,isOpened=False).count()
    return JsonResponse(u,safe=False)

def get_user_notifications(request,id):
    return render(request,'dashboard/messages/notifications.html')

def send_contact_mail(request,id):
    if request.method=='POST':
        e=Etablishment.objects.get(id=id)
        s=request.POST.get('email')
        n=request.POST.get('name')
        o=request.POST.get('subject')
        r=[x for x in str(request.POST.get('contacts')).split(',') if x!=None and x!='']
        print(r,request.POST.get('contacts'))
        m=request.POST.get('message')

        f=f'''E-mail de Contact de IGOguide

        Nom du client : {n}
        Objet du contact : {o}
        E-mail du client : {s}
        Etablissement visité: {e.name}
        Méssage : 
            {m}
        '''

        if send_Mail(
            'VOUS AVEZ ÉTÉ CONTACTÉ DEPUIS IGOGUIDE!',
            f,
            'fiches.igoguide@gmail.com',
            r
        ):
            ContactMail.objects.create(
                subject=o,
                email=s,
                message=m,
                fromUser=int(request.POST.get('fromuser')),
                toUser=e.owner
            )
            return HttpResponse(status=204)

######
###     FAVORIS
######

@csrf_exempt
def save_to_favorites(request):
    
    if request.method=='POST':
        u=User.objects.get(id=request.POST.get('client'))
        e=Etablishment.objects.get(id=request.POST.get('etablishment'))
        f=Favoris.objects.create(
            user=u,
            etablishment=e
        )
        return JsonResponse(f.id,safe=False)
    return JsonResponse('METHOD NOT ALLOWED!',safe=False)

@csrf_exempt
def remove_from_favorites(request,uid,eid):
    if request.method=='DELETE':
        f=Favoris.objects.get(user=int(uid),etablishment=int(eid))
        f.delete()
        return JsonResponse('DELETED',safe=False)

def get_user_favorites(request,id):
    pass

######
###     UTILS
######

def validate(request):

    fields=[x for x in request.POST]
    for i in fields:
        if i==None:
            return False
    return True

def save_media(request,id):
    if request.method=='POST':
        e=Etablishment.objects.get(id=id)
        Media.objects.create(
            name=request.POST.get('description'),
            image=request.FILES.get('image'),
            etablishment=e
        )
    return list_user_etablishments(request,e.owner.id)

def get_subscription_info(request,id):
    d=date.today()+relativedelta(months=int(id))
    r={
        'd':d.ctime(),
        't':int(id)*49.0
    }
    return JsonResponse(r,safe=True)

def get_department_by_id(id):
    et=None
    with open('igoMaster/data/Departments.json','r')as f:
        et=Json.loads(f.read())['Departments']
    for e in et:
        if e['id']==id:
            return e
    return 


def get_forfaits(request):
    l=[{
        'id':f.id,
        'name':f.name,
        'price':f.price,
        'duration':f.duration,
    }for f in Forfait.objects.all()]
    return JsonResponse(l,safe=False)


def send_Mail(obj,msg,emitter,recievers,html=False):
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