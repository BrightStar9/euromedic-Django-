# About
This is the project for one of the leading medical institutions in Balkan region.

### Tech stack

1. Python - Django backend + Django templates
2. PostgreSQL is our DBMS of choice
3. ElasticSearch 7 for search functionalities

# Onboarding
### Using dev containers

If you work with containers in development, you can run the project simply by executing
```bash
docker-compose -f docker-compose.yml up -d --build
```

### Running locally

If you want to run the app locally, suggestion is to still use the containers for Postgres and Elasticsearch.
You can spin them up with
```bash
docker-compose -f docker-compose-local.yml up -d --build
```

### DB Management
You can load the prod DB replica from `tar` file (should be provided by devs), by executing 
```bash
pg_restore -d <db_name> /path/to/your/file/emk.tar -c -U <user>
```
For all new migrations (or if you want to start from scratch), use django management commands
```bash
python manage.py migrate
```

### Elasticsearch
For index management and ES queries, we are using python es wrapper package - [Django Elasticsearch DSL DRF](https://github.com/barseghyanartur/django-elasticsearch-dsl-drf)

Documents are defined in `core/documents`.

You can always repopulate ES from Postgres source by executing django management commands
```bash
python manage.py search_index --create
python manage.py search_index --populate
```

Endpoints for search are currently located in
* core.views.IndexedServicesDocumentViewSet
* core.views.DoctorsDocumentViewSet
* core.views.SearchViewSet 


