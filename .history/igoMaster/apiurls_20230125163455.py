from . import api

#####
#####   ICI SE FAIT LE MAPPING DES URLS EN DIRECTION DE L'API
#####

urlpatterns=[
    ### AUTHENTIFICATION
    path('login/particular/<int:id>', api.AUTH.login)
]