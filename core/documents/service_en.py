from django.conf import settings
from django_elasticsearch_dsl import Index, Document, fields
from elasticsearch_dsl import analyzer, token_filter

from core.models import Service, Category, Hospital, WorkHours, PhoneNumber, Location

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

INDEX.settings(number_of_shards=1, number_of_replicas=0)

html_strip = analyzer(
    "html_strip",
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"],
)

edge_ngram_completion_filter = token_filter(
    "edge_ngram_completion_filter", type="edge_ngram", min_gram=2, max_gram=15
)

edge_ngram_completion = analyzer(
    "edge_ngram_completion",
    tokenizer="standard",
    filter=["lowercase", edge_ngram_completion_filter],
)


@INDEX.doc_type
class ServiceDoc(Document):
    id = fields.IntegerField()
    name = fields.TextField(
        attr="name_en",
        analyzer=edge_ngram_completion,
        search_analyzer="standard",
        fields={
            "raw": fields.KeywordField(),
            "suggest": fields.CompletionField(),
            "edge_ngram_completion": fields.TextField(analyzer=edge_ngram_completion),
        },
    )
    slug = fields.TextField()
    price = fields.FloatField()
    keywords = fields.ListField(
        fields.TextField(
            attr="keyword_list_en",
            analyzer=edge_ngram_completion,
            search_analyzer="standard",
            fields={
                "suggest": fields.CompletionField(multi=True),
                "edge_ngram_completion": fields.TextField(
                    analyzer=edge_ngram_completion
                ),
            },
        )
    )
    category = fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(
                attr="name_en",
                analyzer=edge_ngram_completion,
                fields={
                    "raw": fields.KeywordField(),
                    "suggest": fields.CompletionField(),
                    "edge_ngram_completion": fields.TextField(
                        analyzer=edge_ngram_completion
                    ),
                },
            ),
            "excerpt": fields.TextField(
                attr="excerpt_en",
                analyzer=edge_ngram_completion,
                fields={
                    "raw": fields.KeywordField(),
                    "suggest": fields.CompletionField(),
                    "edge_ngram_completion": fields.TextField(
                        analyzer=edge_ngram_completion
                    ),
                },
            ),
            "description": fields.TextField(attr="description_en", analyzer=html_strip),
        }
    )

    hospitals = fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(
                attr="name_en", fields={"raw": fields.KeywordField()}
            ),
            "description": fields.TextField(attr="description_en", analyzer=html_strip),
            "location": fields.ObjectField(
                properties={
                    "street": fields.TextField(),
                    "number": fields.TextField(),
                    "city": fields.TextField(attr="city_en"),
                    "country": fields.TextField(attr="country_en"),
                    "coordinates": fields.GeoPointField(attr="location_field_indexing"),
                }
            ),
            "transport_buses": fields.TextField(),
            "transport_trams": fields.TextField(),
            "transport_trolleys": fields.TextField(),
            # TODO add type
            "email": fields.TextField(),
            "phone_numbers": fields.ListField(
                fields.TextField(attr="flat_phone_numbers")
            ),
        }
    )

    class Django:
        model = Service
        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        auto_refresh = False

    def get_queryset(self):
        return Service.objects.select_related("category").prefetch_related(
            "hospitals__location", "hospitals__work_hours", "hospitals__phone_numbers"
        )
