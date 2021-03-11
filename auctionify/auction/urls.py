from django.urls import path
from . import views

urlpatterns = [
    path('accounts/signup/', views.SignUpView.as_view(), name="signup"),
    path('update-user-profile/', views.UpdateUserProfile.as_view(), name="update-user-profile"),
    path('create-auction/', views.CreateAuction.as_view(), name="create-auction"),
    path('bid/<str:slug>/', views.BiddingView.as_view(), name="bid"),
]
