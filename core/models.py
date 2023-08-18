from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models, IntegrityError, transaction
from django.utils.text import slugify
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj
from django_better_admin_arrayfield.models.fields import ArrayField


class SluggableModel(models.Model):
    slug = models.CharField(max_length=200, unique=True, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.slug = slugify(getattr(self, self.sluggable_field))
                super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = f"{str(self.pk)}-{slugify(getattr(self, self.sluggable_field))}"
            super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(SluggableModel):
    sluggable_field = "name"
    name = models.CharField(max_length=100, unique=True)
    display_title = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    excerpt = models.TextField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_mobile = models.ImageField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True)
    ordering_id = models.PositiveSmallIntegerField(default=0)
    doctors_ordering_id = models.PositiveSmallIntegerField(default=0)
    grouped_services = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"


class ServiceGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Service(SluggableModel):
    sluggable_field = "name"
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, related_name="services", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        "Standard price. Leave empty if price on demand",
        max_digits=12,
        decimal_places=2,
        default=None,
        null=True,
        blank=True,
    )
    price_extra = models.DecimalField(
        "Upper price. Leave empty if no price range",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    show_price_from = models.BooleanField(default=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    keywords = models.TextField(max_length=1000, null=True, blank=True)
    blog_link = models.CharField(null=True, blank=True, max_length=500)
    ordering_id = models.PositiveSmallIntegerField(default=0)
    service_group = models.ForeignKey(
        ServiceGroup, related_name="services", on_delete=models.SET_NULL, null=True, blank=True
    )
    additional_info = models.TextField(max_length=5000, null=True, blank=True)

    related_services = models.ManyToManyField("self", symmetrical=False, blank=True)

    def keyword_list(self, lang=None):
        attr = "keywords"

        if lang:
            attr += "_" + lang

        as_text = getattr(self, attr)

        if not as_text:
            return []

        return [t.strip() for t in as_text.split(",") if t != ""]

    @property
    def keyword_list_sq(self):
        return self.keyword_list("sq")

    @property
    def keyword_list_en(self):
        return self.keyword_list("en")

    @property
    def keyword_list_sr(self):
        return self.keyword_list("sr")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Location(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    municipality = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    #  TODO switch to geodjango point!
    latitude = models.DecimalField(
        max_digits=16, decimal_places=10, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=16, decimal_places=10, null=True, blank=True
    )
    maps_url = models.TextField(max_length=1000, null=True, blank=True)

    @property
    def location_field_indexing(self):
        """Location for indexing.

        Used in Elasticsearch indexing/tests of `geo_distance` native filter.
        """
        return {"lat": self.latitude, "lon": self.longitude}

    @property
    def display_html_safe(self):
        """
        Pariske komune 22 <br />
        <b>Novi Beograd</b>
        """
        # TODO replace city with new field city_area (Novi Beograd)
        return f"{self.street} {self.number} <br/> <b>{self.city}</b>"

    def __str__(self):
        return "{} {}, {}, {}".format(self.street, self.number, self.city, self.country)


class Image(models.Model):
    img = models.ImageField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class HospitalType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hospital(SluggableModel):
    sluggable_field = "name"
    name = models.CharField(max_length=100)
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.TextField(max_length=1000, null=True, blank=True)
    contact_info = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        help_text="Use this to present any additional contact info"
                  " below the phone numbers. HTML Safe",
    )
    #  TODO remove if categories are enough!!!
    images = GenericRelation(Image)
    hero_image = models.ImageField(null=True, blank=True)
    small_image = models.ImageField(null=True, blank=True)
    transport_buses = models.TextField(max_length=250, null=True, blank=True)
    transport_trams = models.TextField(max_length=250, null=True, blank=True)
    transport_trolleys = models.TextField(max_length=250, null=True, blank=True)
    types = models.ManyToManyField(HospitalType, related_name="hospitals")
    email = models.EmailField(null=True, blank=True)
    services = models.ManyToManyField(Service, related_name="hospitals", blank=True)
    categories = models.ManyToManyField(Category, related_name="hospitals", blank=True)
    ordering_id = models.PositiveSmallIntegerField(default=1000)

    class Meta:
        ordering = ["ordering_id", "id"]

    def __str__(self):
        return self.name

    @property
    def flat_phone_numbers(self):
        return self.phone_numbers.values_list("number", flat=True)

    @property
    def flat_images(self):
        return self.images.values_list("img", flat=True)

    @property
    def ordered_services(self):
        return self.services.prefetch_related("category").order_by("category")

    @property
    def address(self):
        if not self.location:
            return "N/A"
        return f"{self.location.street} {self.location.number}"

    @property
    def display_html_safe(self):
        return self.name.replace("-", "<br/>")


class WorkHours(models.Model):
    hospital = models.OneToOneField(
        Hospital, on_delete=models.CASCADE, related_name="work_hours"
    )
    workdays_start = models.TimeField()
    workdays_end = models.TimeField()
    saturday_start = models.TimeField(null=True, blank=True)
    saturday_end = models.TimeField(null=True, blank=True)
    sunday_start = models.TimeField(null=True, blank=True)
    sunday_end = models.TimeField(null=True, blank=True)

    @property
    def prepare_indexing(self):
        return dict_to_obj(
            {
                "workdays_start": str(self.workdays_start),
                "workdays_end": str(self.workdays_end),
                "saturday_start": str(self.saturday_start),
                "saturday_end": str(self.saturday_end),
                "sunday_start": str(self.sunday_start),
                "sunday_end": str(self.sunday_end),
            }
        )

    class Meta:
        verbose_name_plural = "Work Hours"


class PhoneNumber(models.Model):
    number = models.CharField(max_length=20)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="phone_numbers"
    )

    def __str__(self):
        return self.number


class Bundle(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image = models.ImageField(null=True, blank=True)
    ordering_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["ordering_id"]


class Doctor(SluggableModel):
    sluggable_field = "full_name"

    FEMALE = "F"
    MALE = "M"
    GENDERS = ((FEMALE, "Female"), (MALE, "Male"))

    full_name = models.CharField(max_length=200)
    biography = models.TextField(max_length=2000)
    gender = models.CharField(max_length=1, choices=GENDERS)
    image = models.ImageField(null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True)
    specialization_details = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        related_name="doctors",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    services = ArrayField(
        models.CharField(max_length=200, blank=True), blank=True, default=list
    )
    hospitals = models.ManyToManyField(Hospital, related_name="doctors", blank=True)
    ordering_id = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["ordering_id"]

    @property
    def hospital_ids(self):
        return [h.id for h in self.hospitals.all()]

    @property
    def image_url(self):
        if self.image:
            return self.image.url

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"


class Reference(models.Model):
    description = models.TextField(max_length=500)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="references"
    )

    def __str__(self):
        return f"{self.doctor.full_name} - {self.description}"
