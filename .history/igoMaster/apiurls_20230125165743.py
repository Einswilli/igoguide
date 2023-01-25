from . import api

#####
#####   ICI SE FAIT LE MAPPING DES URLS EN DIRECTION DE L'API
#####

urlpatterns=[
    ### AUTHENTIFICATION
    path('login/particular/<int:id>', api.AUTH.login),
    path('login/professional/<int:id>', api.AUTH.login),
    
    ### PASSWORD
    path('users/changepass/particular/<int:id>', api.AUTH.reset_password),
    path('users/changepass/professional/<int:id>', api.AUTH.reset_password),
    path('users/update/particular/<int:id>', api.AUTH.send_password),
    path('users/update/professional/<int:id>', api.AUTH.send_password),
]