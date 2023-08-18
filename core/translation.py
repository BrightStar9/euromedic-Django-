from modeltranslation.translator import register, TranslationOptions

from core.models import Category, Service, Hospital, Location, HospitalType


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "excerpt", "description")


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name", "keywords")


@register(Location)
class LocationTranslationOptions(TranslationOptions):
    fields = ("city", "country", "municipality")


@register(Hospital)
class HospitalTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(HospitalType)
class HospitalTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
