from django.conf import settings
from django_elasticsearch_dsl import Index, Document, fields
from elasticsearch_dsl import analyzer, token_filter

from core.models import Doctor

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

INDEX.settings(number_of_shards=1, number_of_replicas=0)

edge_ngram_completion_filter = token_filter(
    "edge_ngram_completion_filter", type="edge_ngram", min_gram=3, max_gram=15
)

edge_ngram_completion = analyzer(
    "edge_ngram_completion",
    tokenizer="standard",
    filter=["lowercase", "asciifolding", "snowball", edge_ngram_completion_filter],
)


@INDEX.doc_type
class DoctorDoc(Document):
    id = fields.IntegerField()
    full_name = fields.TextField(
        attr="full_name",
        analyzer=edge_ngram_completion,
        fields={
            "raw": fields.KeywordField(),
            "suggest": fields.CompletionField(analyzer=edge_ngram_completion),
            "edge_ngram_completion": fields.TextField(analyzer=edge_ngram_completion),
        },
    )
    slug = fields.TextField()
    biography = fields.TextField()
    specialization = fields.TextField()
    image_url = fields.TextField()
    specialization_details = fields.TextField()
    category = fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(
                attr="name_sr",
                analyzer=edge_ngram_completion,
                fields={
                    "raw": fields.KeywordField(),
                    "suggest": fields.CompletionField(),
                    "edge_ngram_completion": fields.TextField(
                        analyzer=edge_ngram_completion
                    ),
                },
            ),
            "display_title": fields.TextField(),
        }
    )
    ordering_id = fields.IntegerField()
    hospitals = fields.ListField(fields.IntegerField(attr="hospital_ids"))

    class Django:
        model = Doctor
        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        ignore_signals = False
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = True

    def get_queryset(self):
        return Doctor.objects.select_related("category").prefetch_related("hospitals")
