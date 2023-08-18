from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from core import views, frontend

router = DefaultRouter(trailing_slash=True)

router.register(
    "search-services", views.IndexedServicesDocumentViewSet, basename="search-services"
)
router.register(
    "search-doctors", views.DoctorsDocumentViewSet, basename="search-doctors"
)
router.register("search", views.SearchViewSet, basename="search")
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("services", views.ServiceViewSet, basename="services")
router.register("hospitals", views.HospitalViewSet, basename="hospitals")

urlpatterns = [
    path("usluga/<slug:slug>/", frontend.ServiceView.as_view(), name="services-detail"),
    path("usluge/", frontend.CategoriesView.as_view(), name="categories"),
    path(
        "usluge/<slug:slug>/", frontend.CategoryView.as_view(), name="categories-detail"
    ),
    path("cenovnik/", frontend.PricingView.as_view(), name="pricing"),
    path("lokacije/", frontend.HospitalsView.as_view(), name="hospitals"),
    path(
        "lokacije/<slug:slug>/",
        frontend.HospitalView.as_view(),
        name="hospitals-detail",
    ),
    path("paketi-pregleda/", frontend.BundlesView.as_view(), name="review-packages"),
    path(
        "kontakt/",
        TemplateView.as_view(template_name="contact.html"),
        name="contact-us",
    ),
    path("lekari/", frontend.DoctorsView.as_view(), name="doctors"),
    path("lekari/<slug:slug>/", frontend.DoctorView.as_view(), name="doctors-detail"),
    path("", frontend.IndexView.as_view(), name="index"),
]
