from django.urls import path
from . import views

#####
#####   ICI P designe particulier et PRO designe professionnel
#####

urlpatterns=[

    ###     ACCUEIL
    path("",views.home,name="Home"),
    path("dashboard",views.dashboard,name='dashboard'),

    ###     FAQ - CGV - CGU
    path("faq",views.faq),
    path("cgv",views.cgv),
    path("cgu",views.cgu),
    path("cgu_footer", views.cgu_footer),
    path("faq_footer", views.faq_footer),

    ### Médias
    path('media/new/<int:id>',views.save_media),

    ### Forfaits
    path('forfaits/',views.get_forfaits),

    ### Favoris
    path('favorites/new',views.save_to_favorites),
    path('favorites/delete/<int:uid>/<int:eid>',views.remove_from_favorites),
    path('redirect/to/login',views.particular_auth),

    ### Mails
    path('mails/pro/<int:id>',views.get_user_mails),
    path('notifications/pro/<int:id>',views.get_user_notifications),
    path('mails/contact/<int:id>',views.send_contact_mail),
    path('mails/unreads/pro/<int:id>',views.get_user_unread_mails_count),
    path('mails/<int:id>',views.get_mailX),

    ###    Connexions et Authentifications 
    ###    I- Côté particulier.
    path('auth/p/connexion',views.particular_auth,name='particular_login'),
    path('auth/p/login',views.particular_login,name='p_login'),
    path('auth/p/new',views.new_particular,name='new_particular'),
    path('auth/p/register',views.particular_register,name='particular_register'),
    path('pass/reset',views.pass_reset),
    path('pass',views.send_pass,name='send_pass'),

    ### II- Côté professionnel
    path('auth/pro/connexion',views.professional_auth,name="professional_login"),
    path('auth/pro/login',views.professional_login,name="pro_login"),
    path('auth/pro/new',views.new_professional,name="new_professional"),
    path('auth/pro/register',views.professional_register,name="professional_register"),
    path('auth/pro/logout',views.pro_logout),
    path('auth/p/logout',views.p_logout),

    ### Catégories d'établissements
    path('categorie/<int:id>',views.get_categorieX),

    ### Etablissements
    ###     I- Dashboard
    path('etablishment/new',views.new_etablishment),
    path('etablishment/save',views.save_etablishment),
    path('etablishment/<int:id>',views.get_etablishment_details),
    path('etablishment/list/pro/<int:id>',views.list_user_etablishments,name="user_etablishments"),
    path('etablishment/get/pro/<int:id>',views.get_user_etablishments),
    path('etablissement/edit/<int:id>',views.edit_etablishment),
    path('etablissement/delete/<int:id>',views.delete_etablishment),
    ###     II- Filtres
    path('etablishment/subtype/<int:id>',views.list_subtypeX_etablishment),
    path('etablishment/search',views.search_etablishment),
    path('etablishment/dept/<int:id>',views.get_dept_etablishments),
    path('etablishment/reg/<str:reg>',views.get_reg_etablishments),

    ### ABONNEMENTS
    path('subscription/new',views.new_subscription),
    path('subscription/save',views.save_subscription),
    path('subscription/list/pro/<int:id>',views.list_user_subscriptions),
    path('subscription/info/<int:id>',views.get_subscription_info),
    path('payments/new/<int:id>',views.new_payment),
    path('payments/pro/<int:id>',views.list_user_payments),

    ### UTILISATEURS
    path('users/p/<int:id>',views.get_particular_user),
    path('users/pro/<int:id>',views.get_professional_user),
    path('profile/pro/<int:id>',views.get_user_profile),
    path('profile/p/<int:id>',views.get_particular_profile),
    path('users/changepass/p/<int:id>',views.change_userp_pass),
    path('users/changepass/pro/<int:id>',views.change_userpro_pass),
    path('users/update/p/<int:id>',views.update_userp),
    path('users/update/pro/<int:id>',views.update_userpro)
]