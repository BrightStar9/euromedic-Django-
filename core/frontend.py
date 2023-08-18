from django.db.models import Prefetch, Q, Count
from django.views import generic

from core.models import (
    Hospital,
    Category,
    Service,
    Bundle,
    PhoneNumber,
    Doctor,
    Reference,
)


class IndexView(generic.ListView):
    model = Hospital
    template_name = "index.html"
    context_object_name = "hospitals"

    def get_queryset(self):
        return (
            Hospital.objects.select_related("location")
            .prefetch_related("images")
            .all()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            Category.objects.filter(parent__isnull=True)
            .prefetch_related("children")
            .all()
        )
        return context


class ServiceView(generic.DetailView):
    model = Service
    context_object_name = "service"
    template_name = "service.html"

    def get_object(self, queryset=None):
        slug_field = self.get_slug_field()
        slug = self.kwargs.get(self.slug_url_kwarg)

        return (
            Service.objects.filter(**{slug_field: slug})
            .prefetch_related(
                Prefetch(
                    "hospitals",
                    queryset=Hospital.objects.select_related("location")
                    .prefetch_related("phone_numbers"),
                )
            )
            .first()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoriesView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = "categories.html"

    def get_queryset(self):
        return (
            Category.objects.filter(parent__isnull=True)
            .prefetch_related(
                Prefetch(
                    "children",
                    queryset=Category.objects.order_by("ordering_id")
                    .annotate(num_services=Count("services"))
                    .filter(num_services__gt=0)
                    .all(),
                )
            )
            .order_by("ordering_id")
            .all()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryView(generic.DetailView):
    model = Category
    context_object_name = "category"
    template_name = "category.html"

    def get_queryset(self):
        return (
            Category.objects.prefetch_related(
                Prefetch(
                    "services", queryset=Service.objects.order_by("ordering_id", "service_group_id").all()
                )
            )
            .order_by("ordering_id")
            .all()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["category"]
        group_map = {}

        if category.grouped_services:
            for s in category.services.all():
                k = s.service_group.title
                if not group_map.get(k):
                    group_map[k] = [s]
                else:
                    group_map[k].append(s)

        context["group_map"] = group_map
        return context


class PricingView(generic.TemplateView):
    template_name = "pricing.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            Category.objects.annotate(service_count=Count("services"))
            .filter(service_count__gt=0)
            .filter(parent__isnull=False)
            .prefetch_related(
                Prefetch(
                    "services", queryset=Service.objects.order_by("ordering_id").all()
                )
            )
            .order_by("ordering_id")
            .all()
        )
        context["hospitals"] = Hospital.objects.all()
        return context


class HospitalsView(generic.ListView):
    model = Hospital
    context_object_name = "hospitals"
    template_name = "hospitals.html"


class HospitalView(generic.DetailView):
    model = Hospital
    context_object_name = "hospital"
    template_name = "hospital.html"

    def get_queryset(self):
        return Hospital.objects.prefetch_related("services__category", "phone_numbers")

    def get_context_data(self, *, object_list=None, **kwargs):
        hospital = self.get_object()
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            Category.objects.filter(services__in=hospital.services.all())
            .distinct()
            .order_by("ordering_id")
        )
        return context


class BundlesView(generic.ListView):
    model = Bundle
    context_object_name = "bundles"
    template_name = "review-packages.html"

    def get_queryset(self):
        return Bundle.objects.select_related("service")


class DoctorView(generic.DetailView):
    model = Doctor
    context_object_name = "doctor"
    template_name = "doctor.html"

    def get_object(self, queryset=None):
        slug_field = self.get_slug_field()
        slug = self.kwargs.get(self.slug_url_kwarg)

        return (
            Doctor.objects.filter(**{slug_field: slug})
            .prefetch_related(
                Prefetch("references", queryset=Reference.objects.all()),
                Prefetch(
                    "hospitals",
                    queryset=Hospital.objects.select_related("location")
                    .prefetch_related("phone_numbers"),
                ),
            )
            .first()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DoctorsView(generic.ListView):
    model = Doctor
    context_object_name = "doctors"
    template_name = "doctors.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            Category.objects.distinct()
            .annotate(doctor_count=Count("doctors"))
            .filter(doctor_count__gt=0)
            .prefetch_related(
                Prefetch("doctors", queryset=Doctor.objects.order_by("ordering_id"))
            )
            .order_by("doctors_ordering_id")
            .all()
        )

        context["single_categories"] = [
            (
                Category.objects.distinct()
                .annotate(doctor_count=Count("doctors"))
                .filter(doctor_count__gt=0)
                .prefetch_related(
                    Prefetch("doctors", queryset=Doctor.objects.order_by("ordering_id"))
                )
                .order_by("doctors_ordering_id")
                .first()
            )
        ]
        context["hospitals"] = Hospital.objects.all()
        return context
