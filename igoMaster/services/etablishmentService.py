from ..models import *
from ..exceptions import *
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class EtablishmentService:

    def save(self, request):

        other_ctx={}    #POUR LES INFOS DIVERSES

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

        return e.to_json()

    def show(self,id):
        #   RENVOIE L'ETABLISSEMENT AVEC L'ID S'IL EXISTE

        try:
            return Etablishment.objects.get(id=id).to_json()
        except:
            #   ETABLISSEMENT INTROUVVABLE
            return ObjectNotFoundException('ETABLISHMENT', id).format()

    def list(self):
        # RENVOIE LA LISTE DES ETABLISSEMENTS

        return[
            e.to_json() for e in Etablishment.objects.all()
        ]

    def update(self,request,id):
        #   MET A JOUR UN ETABLISSEMENT

        try:
            e=Etablishment.objects.get(id=id)

            # RECUPERATION ET ENREGSTREMENT
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
        except:
            return ObjectNotFoundException('ETABLISHMENT',id).format()

    def get_medias(self,id):
        # RENVOIE LES IMAGES DE L'ETABLISSEMENT AVEC L'ID

        try:
            return Etablishment.objects.get(id=id).get_medias()
        except:
            #   ETABLISSEMENT INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()

    def get_contacts(self,id):
        # RENVOIE LA LISTE DES CONTACTS DE L'ETABLISSEMENT AVEC L'ID

        try:
            return Etablishment.objects.get(id=id).get_contacts()
        except:
            # ETABLISSEMENT INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()

    def get_subscriptions(self,id):
        #   RENVOIE LA LISTE DES ABONNEMENTS DE L'ETABLISSEMENT AVEC L'ID

        try:
            return Etablishment.objects.get(id=id).get_subscriptions()
        except:
            #   ETABLISSEMENT INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()

    def get_socials(self,id):
        # RENVOIE LA LISTE DES RESEAUX SOCIAUX DE L'ETABLISSECTION AVEC L'ID
        
        try:
            return Etablishment.objects.get(id=id).get_socials()
        except:
            # ETABLISSECTION INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()

    def get_others(self,id):
        # RENVOIE LA LISTE DES INFOS DIVERSES DE L'ETABLISSEMENT AVEC L'ID

        try:
            return Etablishment.objects.get(id=id).get_others()
        except:
            # ETABLISSECTION INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()

    def get_promotions(self,id):
        #   RENVOIE LA LISTE DES PROMOTIONS DE L'ETABLISSECTION AVEC L'ID

        try:
            return Etablishment.objects.get(id=id).get_promotions()
        except:
            # ETABLISSECTION INTROUVABLE!
            return ObjectNotFoundException('ETABLISHMENT',id).format()