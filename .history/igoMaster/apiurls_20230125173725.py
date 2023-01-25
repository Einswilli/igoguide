from . import api

#####
#####   ICI SE FAIT LE MAPPING DES URLS EN DIRECTION DE L'API
#####

urlpatterns=[
    #####
    #####   AUTHENTIFICATION
    #####
    path('login/particular/<int:id>', api.AUTH.login),
    path('login/professional/<int:id>', api.AUTH.login),
    
    #####
    #####   MOTS DE PASSES
    #####
    path('users/changepass/particular/<int:id>', api.AUTH.reset_password),
    path('users/changepass/professional/<int:id>', api.AUTH.reset_password),
    path('users/update/particular/<int:id>', api.AUTH.send_password),
    path('users/update/professional/<int:id>', api.AUTH.send_password),

    #####
    #####   LES TYPES D'UTILISATEURS
    #####
    path('usertype/new', api.USERTYPE.save),
    path('usertype/update/<int:id>', api.USERTYPE.update),
    path('usertype/list', api.USERTYPE.list),
    path('usertype/get/<int:id>', api.USERTYPE.get_members),
    path('usertype/show/<int:id>', api.USERTYPE.show),

    ### LES UTILISATEURS
    path('user/new', api.USER.save),
    path('user/update/<int:id>', api.USER.update),
    path('user/list', api.USER.list),
    path('user/show/<int:id>', api.USER.show),
    path('user/delete/<int:id>', api.USER.delete),
        ### LES FAVORIES DES UTILISATEURS
    path('user/favoris/save', api.USER.add_favoris),
    path('user/favoris/getAll/<int:id>', api.USER.get_favoris),
    path('user/favoris/remove/<int:uid>/<int:eid>', api.USER.remove_favoris),
        ### MAILS && NOTIFICATIONS DES UTILISATEURS
    path('user/mail/get/<int:id>', api.USER.get_mails),
    path('user/mail/get/<int:id>', api.USER.get_notifications),
        ### LES ETABLISSEMENTS DES UTILISATEURS
    path('user/etablishment/get/<int:id>', api.USER.get_etablissements),

    ###
]