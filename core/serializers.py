import copy
from collections import OrderedDict

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import get_language
from django_elasticsearch_dsl_drf.helpers import sort_by_list
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from django_elasticsearch_dsl_drf.utils import EmptySearch
from rest_framework import serializers
from rest_framework.fields import empty

from core.documents.doctor import DoctorDoc
from core.documents.service_en import ServiceDoc as ServiceDocumentEn
from core.documents.service_sq import ServiceDoc as ServiceDocumentSq
from core.documents.service_sr import ServiceDoc as ServiceDocumentSr
from core.models import Service, Category, Location, WorkHours, PhoneNumber, Hospital


class ReadOnlyCustomImageField(serializers.FileField):
    def to_representation(self, value):
        value = value.img
        if not value:
            return None
        if not getattr(value, "url", None):
            # If the file has not been saved it may not have a URL.
            return None
        url = value.url
        request = self.context.get("request", None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class LocationSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    def get_coordinates(self, obj):
        return obj.location_field_indexing

    class Meta:
        model = Location
        fields = ("id", "street", "number", "city", "country", "coordinates")


class WorkHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHours
        fields = "__all__"


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"


class HospitalSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    phone_numbers = PhoneNumberSerializer(many=True)
    work_hours = WorkHoursSerializer()
    images = serializers.ListSerializer(child=ReadOnlyCustomImageField())

    class Meta:
        model = Hospital
        fields = (
            "id",
            "name",
            "description",
            "location",
            "work_hours",
            "phone_numbers",
            "images",
            "hero_image",
            "transport_buses",
            "transport_trams",
            "transport_trolleys",
            "is_hospital",
            "is_health_center",
            "is_stationary",
            "email",
        )


class NakedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "excerpt",
            "description",
            "image",
            "image_mobile",
            "icon",
        )


class SkinnyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "excerpt",
            "description",
            "image",
            "image_mobile",
            "icon",
            "hospitals",
            "services",
        )


class ServiceSerializer(serializers.ModelSerializer):
    hospitals = HospitalSerializer(many=True)
    category = SkinnyCategorySerializer()

    class Meta:
        model = Service
        fields = ("id", "name", "price", "category", "hospitals")


class SkinnyServiceSerializer(serializers.ModelSerializer):
    # hospitals = HospitalSerializer(many=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "price",
            # 'hospitals',
        )


class CategorySerializer(serializers.ModelSerializer):
    services = SkinnyServiceSerializer(many=True)
    hospitals = HospitalSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "excerpt",
            "description",
            "image",
            "image_mobile",
            "icon",
            "hospitals",
            "services",
        )


class ServiceForHospitalsSerializer(serializers.ModelSerializer):
    category = NakedCategorySerializer()

    class Meta:
        model = Service
        fields = ("id", "name", "price", "category")


class FullHospitalSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    phone_numbers = serializers.ListSerializer(child=serializers.CharField())
    work_hours = WorkHoursSerializer()
    services = ServiceForHospitalsSerializer(many=True)
    images = serializers.ListSerializer(child=ReadOnlyCustomImageField())

    class Meta:
        model = Hospital
        fields = (
            "id",
            "name",
            "description",
            "location",
            "services",
            "work_hours",
            "phone_numbers",
            "images",
            "hero_image",
            "transport_buses",
            "transport_trams",
            "transport_trolleys",
            "is_hospital",
            "is_health_center",
            "is_stationary",
            "email",
        )


class TranslatableDocumentSerializer(DocumentSerializer):
    _abstract = True

    def __init__(self, instance=None, data=empty, **kwargs):
        if (
            not hasattr(self.Meta, "localized_documents")
            or self.Meta.localized_documents is None
        ):
            raise ImproperlyConfigured(
                "You must set the 'localized_documents' dict on the serializer "
                "Meta class."
            )

        if not isinstance(self.Meta.localized_documents, dict):
            raise ImproperlyConfigured(
                "localized_documents must be a dict instance" "class."
            )

        super().__init__(instance, data, **kwargs)

        if not self.instance:
            self.instance = EmptySearch()

    def get_document(self):
        request_lang = get_language()

        return self.Meta.localized_documents.get(request_lang, self.Meta.document)

    def get_fields(self):
        """Get the required fields for serializing the result."""
        __fields = self.Meta.fields
        exclude = self.Meta.exclude
        ignore_fields = self.Meta.ignore_fields
        document = self.get_document()
        model = document.Django.model
        document_fields = document._fields

        declared_fields = copy.deepcopy(self._declared_fields)
        field_mapping = OrderedDict()

        for field_name, field_type in document_fields.items():
            orig_name = field_name[:]

            # Don't use this field if it is in `ignore_fields`
            if orig_name in ignore_fields or field_name in ignore_fields:
                continue
            # When fields to include are decided by `exclude`
            if exclude:
                if orig_name in exclude or field_name in exclude:
                    continue
            # When fields to include are decided by `fields`
            if __fields:
                if orig_name not in __fields and field_name not in __fields:
                    continue

            # Look up the field attributes on the current index model,
            # in order to correctly instantiate the serializer field.

            kwargs = self._get_default_field_kwargs(model, field_name, field_type)
            # If field not in the mapping, just skip
            if field_type.__class__ not in self._field_mapping:
                continue

            field_mapping[field_name] = self._field_mapping[field_type.__class__](
                **kwargs
            )

        # Add any explicitly declared fields. They *will* override any index
        # fields in case of naming collision!.
        if declared_fields:
            for field_name in declared_fields:
                field_mapping[field_name] = declared_fields[field_name]

        field_mapping = sort_by_list(field_mapping, __fields)
        return field_mapping


class ServiceDocumentSerializer(TranslatableDocumentSerializer):
    class Meta:
        document = ServiceDocumentSr

        localized_documents = {
            "sr": ServiceDocumentSr,
            "en": ServiceDocumentEn,
            "sq": ServiceDocumentSq,
        }


class DoctorDocumentSerializer(DocumentSerializer):
    class Meta:
        document = DoctorDoc


class ServiceDocSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    price = serializers.FloatField()


class DoctorDocSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    slug = serializers.CharField()


class MultiSearchSerializer(serializers.Serializer):
    services = ServiceDocSerializer(many=True)
    doctors = DoctorDocSerializer(many=True)
