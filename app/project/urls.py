""" url mapping for project app"""

from django.urls import (
    path,
    include,
)

from project.views import (ProjectListView,ProjectInstanceList,
                           ProjectDetailView,UserListView,
                           ProjectInstanceDetail,TabInstanceList)


from rest_framework import routers
router = routers.DefaultRouter()
router.register('', TabInstanceList, basename='tab_instance_list')


urlpatterns = [
    path('',UserListView.as_view(),name = 'user-list'),
    path('<company_name>/',ProjectListView.as_view(),name='project-list'),
    path('<company_name>/<project_title_slug>/',ProjectDetailView.as_view(), name='project-detail'),
    path('<company_name>/<project_title_slug>/projectinstances/',ProjectInstanceList.as_view(),
         name='projectinstance-list'),
    path('<company_name>/<project_title_slug>/<project_instance_slug>/',ProjectInstanceDetail.as_view(),
         name='projectinstance-detail'),
    path('<company_name>/<project_title_slug>/<project_instance_slug>/tabinstances/',
         include(router.urls)),

    #path('projects/projectinstances',ProjectInstanceList.as_view(),name='projectinstance-list'),
]














# """ url mapping for recipe app"""

# from django.urls import (
#     path,
#     include,
# )

# from rest_framework.routers import DefaultRouter

# from recipe import views

# router = DefaultRouter()
# router.register('recipes',views.RecipeViewSet)
# """ Recipe view set will have auto generated URLs """
# router.register('tags',views.TagViewSet)
# router.register('ingredients',views.IngredientViewSet)

# app_name = 'recipe'

# urlpatterns = [
#     path('',include(router.urls)),
# ]