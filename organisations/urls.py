from django.urls import path, include

from organisations.views import organisation as organisation_view
from organisations.views import user as user_view
from organisations.views import country as country_view

country_pattern = [
    # list of all countries
    path('', country_view.country_list, name="country_list"),
    # create and store new country form,
    path('create', country_view.create_country, name="create_country"),
    # store new country
    # path('store/', country_view.store_country, name="store_country"),
    # show country
    path('<int:country_id>/', country_view.show_Country, name="show_country"),
    # edit and update country form
    path('<int:country_id>/edit', country_view.edit_country, name="edit_country"),
    # update country
    # path('<int:country_id>/update', country_view.edit_country, name="update_country"),
    # delete country
    path('<int:country_id>/delete', country_view.delete_country, name="delete_country")
]

organisations_pattern = [
    # list all church location branches
    path('', organisation_view.organisation_list, name="organisation_list"),
    # create new church location branch [ store view is merge with create view]
    path('create/', organisation_view.create_organisation, name="create_organisation"),
    # store new church location branch
    # path('store/', organisation_view.store_organisation, name="store_organisation"),
    # show church location branch
    path('<int:organisation_id>/', organisation_view.show_organisation, name="show_organisation"),
    # edit and update chruch location branch
    path('<int:organisation_id>/edit', organisation_view.edit_and_update_organisation, name="edit_and_update_org"),
    # delete organisation
    path('<int:organisation_id>/delete', organisation_view.delete_organisation, name="delete_organisation")
]

user_pattern = [
    # user list
    path('', user_view.user_list, name="user_list"),
    # create user
    # path('create/', user_view.create_user, name="create_user"),
    #  crearte is merge to store new user
    path('create/', user_view.store_user, name="create_user"),
    # show user
    path('<int:user_id>/', user_view.show_user, name="show_user"),
    path('<int:user_id>/reactivate', user_view.reactivate_user, name="activate_user"),
    path('<int:user_id>/deactivate', user_view.deactivate_user, name="deactivate_user"),
    # edit and update
    path('<int:user_id>/update', user_view.update_user, name="update_user"),
    # delete user
    path('<int:user_id>/delete', user_view.delete_user, name="delete_user")
]

# only admin can do this
urlpatterns = [
    path('centimedia/organisations/', include(organisations_pattern)),
    path('centimedia/countries/', include(country_pattern)),
    path('centimedia/users/', include(user_pattern))
]
