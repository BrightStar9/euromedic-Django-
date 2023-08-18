from django.conf import settings
from django.utils.translation import get_language
from django_elasticsearch_dsl_drf.constants import FUNCTIONAL_SUGGESTER_COMPLETION_MATCH
from django_elasticsearch_dsl_drf.filter_backends import (
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
    FunctionalSuggesterFilterBackend,
    NestedFilteringFilterBackend,
    FilteringFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import Search
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from core import serializers
from core.documents.doctor import DoctorDoc
from core.models import Category, Service, Hospital
from core.serializers import (
    ServiceDocumentSerializer,
    MultiSearchSerializer,
    DoctorDocumentSerializer,
)


class CategoryViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return Category.objects.prefetch_related(
            "services",
            "hospitals__location",
            "hospitals__work_hours",
            "hospitals__phone_numbers",
            "hospitals__images",
        ).all()


class ServiceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ServiceSerializer

    def get_queryset(self):
        return (
            Service.objects.select_related("category")
            .prefetch_related(
                "hospitals__location",
                "hospitals__work_hours",
                "hospitals__phone_numbers",
                "hospitals__images",
            )
            .all()
        )


class HospitalViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.FullHospitalSerializer

    def get_queryset(self):
        return (
            Hospital.objects.select_related("work_hours")
            .prefetch_related("services__category", "phone_numbers")
            .all()
        )


class IndexedServicesDocumentViewSet(DocumentViewSet):
    serializer_class = ServiceDocumentSerializer

    filter_backends = [
        OrderingFilterBackend,
        FilteringFilterBackend,
        NestedFilteringFilterBackend,
        CompoundSearchFilterBackend,
        DefaultOrderingFilterBackend,
        FunctionalSuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination

    # Define filtering fields
    filter_fields = {"id": {"field": "id"}}
    # Nested filtering fields
    nested_filter_fields = {
        "n_category": {"field": "category.id", "path": "category"},
        "n_hospital": {"field": "hospitals.id", "path": "hospitals"},
    }

    # Define search fields
    search_fields = {
        "name": {"boost":8},
        "keywords": {"boost":1},
    }

    
    # Define ordering fields
    ordering_fields = {
        "id": None,
        "name": None,
        "category": "category.name",
        "hospital": "hospitals.name",
    }

    #ordering = ("id",)

    functional_suggester_fields = {
        "name_suggest": {
            "field": "name.edge_ngram_completion",
            "suggesters": [FUNCTIONAL_SUGGESTER_COMPLETION_MATCH],
            "default_suggester": FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            "options": {"size": 25, "from": 0},  # Number of suggestions to retrieve.
        },
        "keywords_suggest": {
            "field": "keywords.edge_ngram_completion",
            "suggesters": [FUNCTIONAL_SUGGESTER_COMPLETION_MATCH],
            "default_suggester": FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            "options": {"size": 25, "from": 0},  # Number of suggestions to retrieve.
        },
    }

    def get_document(self):
        request_lang = get_language()

        return self.serializer_class.Meta.localized_documents.get(
            request_lang, self.serializer_class.Meta.document
        )

    def __init__(self, *args, **kwargs):
        self.document = self.get_document()
        super().__init__(*args, **kwargs)


class DoctorsDocumentViewSet(DocumentViewSet):
    serializer_class = DoctorDocumentSerializer
    document = DoctorDoc

    filter_backends = [
        OrderingFilterBackend,
        FilteringFilterBackend,
        NestedFilteringFilterBackend,
        CompoundSearchFilterBackend,
        DefaultOrderingFilterBackend,
        FunctionalSuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination

    # Define filtering fields
    filter_fields = {"id": {"field": "id"}, "n_hospital": {"field": "hospitals"}}

    nested_filter_fields = {"n_category": {"field": "category.id", "path": "category"}}

    # Define search fields
    search_fields = {"full_name": {"boost": 6}}
    # Define ordering fields
    ordering_fields = {"id": None, "full_name": None}

    ordering = ()

    functional_suggester_fields = {
        "name_suggest": {
            "field": "full_name.edge_ngram_completion",
            "suggesters": [FUNCTIONAL_SUGGESTER_COMPLETION_MATCH],
            "default_suggester": FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            "options": {"size": 1, "from": 0},  # Number of suggestions to retrieve.
        }
    }


class SearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MultiSearchSerializer
    pagination_class = None

    def _build_queryset(self, services, doctors):
        qs = {"services": [], "doctors": []}

        for s in services["hits"]["hits"]:
            qs["services"].append(s["_source"])

        for s in doctors["hits"]["hits"]:
            qs["doctors"].append(s["_source"])

        return qs

    def get_queryset(self):
        service_search = Search(
            index=settings.ELASTICSEARCH_INDEX_NAMES["core.documents.service_sr"]
        )
        service_query = service_search.query(
            "multi_match",
            query=self.request.query_params.get("q"),
            fields=["keywords^2", "name^1"],
        )
        services = service_query.execute()

        doctor_search = Search(
            index=settings.ELASTICSEARCH_INDEX_NAMES["core.documents.doctor"]
        )
        doctor_query = doctor_search.query(
            "multi_match",
            query=self.request.query_params.get("q"),
            fields=["full_name^3", "biography^1"],
        )
        doctors = doctor_query.execute()

        return self._build_queryset(services.to_dict(), doctors.to_dict())

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
