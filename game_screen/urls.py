from django.urls import path
from game_screen import views

urlpatterns = [
    path('select-game-category', views.select_game_category, name='select-game-category'),
    path('select-game-level/<str:game_category_id>', views.select_game_level, name='select-game-level'),
    path('select-game/<str:game_category_id>/<str:game_level_id>', views.select_game, name='select-game'),
    path('start-game/<str:game_id>', views.start_game, name='start-game'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.homepage, name='homepage')
]
