from euromedic.settings import *

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = [
#     # TODO ADD DOMAIN!!!
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

# Name of the Elasticsearch index
ELASTICSEARCH_INDEX_NAMES = {
    # TODO make dynamic
    "core.documents.service_sr": "service_sr",
    "core.documents.service_en": "service_en",
    "core.documents.service_sq": "service_sq",
    "core.documents.doctor": "doctor",
}

MEDIA_URL = "/media/"

COMPRESS_OFFLINE = True
LIBSASS_OUTPUT_STYLE = "compressed"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
