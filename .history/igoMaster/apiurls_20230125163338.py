from . import api

#####
#####   ICI SE FAIT LE MAPPING DES URLS EN DIRECTION DE L'API
#####

urlpatterns=[
    ### AUTHENTIFICATION
    path('users/particular/<int:id>', api.AUTH)
]