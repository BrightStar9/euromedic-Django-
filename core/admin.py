from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from modeltranslation.admin import TranslationAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from core.models import *


class WorkHoursInline(admin.TabularInline):
    model = WorkHours


class PhoneNumberInline(admin.StackedInline):
    model = PhoneNumber


class ServiceInline(admin.TabularInline):
    model = Service


class ServiceHospitalInline(admin.StackedInline):
    model = Service.hospitals.through


class RelatedServicesInline(admin.StackedInline):
    model = Service.related_services.through
    fk_name = 'from_service'
    raw_id_fields = ('to_service',)


class ImageHospitalInline(GenericStackedInline):
    model = Image


class CategoryAdmin(TranslationAdmin):
    inlines = (ServiceInline,)
    search_fields = ("name_sr",)


class ServiceAdmin(TranslationAdmin):
    inlines = (ServiceHospitalInline, RelatedServicesInline,)
    search_fields = ("name_sr", "category__name_sr")


class HospitalAdmin(TranslationAdmin):
    inlines = (WorkHoursInline, PhoneNumberInline, ImageHospitalInline)


class LocationAdmin(TranslationAdmin):
    pass


class HospitalTypeAdmin(TranslationAdmin):
    pass


class ReferenceInline(admin.TabularInline):
    model = Reference


class DoctorAdmin(admin.ModelAdmin, DynamicArrayMixin):
    inlines = (ReferenceInline,)


# Register your models here.
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(HospitalType, HospitalTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Doctor, DoctorAdmin)

admin.site.register(PhoneNumber)
admin.site.register(WorkHours)
admin.site.register(Bundle)
admin.site.register(Reference)
admin.site.register(ServiceGroup)
