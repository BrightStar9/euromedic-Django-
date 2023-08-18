import datetime
import math

import pandas as pd
from django.core.management.base import BaseCommand

from core.models import Hospital, Category, Service, Location, HospitalType, WorkHours


class Command(BaseCommand):
    help = "Migrates service data from xls file"

    def add_arguments(self, parser):
        parser.add_argument("path")

    def import_hospitals(self, hospitals):
        self.stdout.write("Migrating the sheet: HOSPITALS")
        for index, row in hospitals.iterrows():
            loc_data = {
                "street": row["Street"],
                "number": row["number"],
                "latitude": row["lat"],
                "longitude": row["long"],
                "city": "Beograd",
                "country": "Srbija",
            }
            location = Location.objects.create(**loc_data)
            types_row = row["Tip"]
            types_list = types_row.replace(" ", "").split(",")
            types = [HospitalType.objects.get_or_create(name=t)[0] for t in types_list]
            data = {"name": row["Name"].strip(), "location": location}
            hospital = Hospital.objects.create(**data)
            hospital.types.set(types)
            hospital.save()

            print(row["sunday_start"])
            hrs = {
                "hospital": hospital,
                "workdays_start": row["workdays_start"],
                "workdays_end": row["workdays_end"],
                "saturday_start": row["saturday_start"],
                "saturday_end": row["saturday_end"],
                "sunday_start": row["sunday_start"]
                if isinstance(row["sunday_start"], datetime.time)
                else None,
                "sunday_end": row["sunday_end"]
                if isinstance(row["sunday_end"], datetime.time)
                else None,
            }
            WorkHours.objects.create(**hrs)

    def import_categories(self, categories):
        self.stdout.write("Migrating the sheet: CATEGORIES")

        for index, row in categories.iterrows():
            parent, _ = Category.objects.get_or_create(
                name=row["Nadkategorija"].strip()
            )
            data = {"parent": parent, "name": row["Kategorija"].strip()}
            Category.objects.create(**data)

    def import_services(self, services):
        self.stdout.write("Migrating the sheet: SERVICES")

        for index, row in services.iterrows():
            cat = Category.objects.get(name__iexact=row["Kategorija"].strip())
            self.stdout.write("Migrating the service {}".format(row["ime usluge"]))
            hospitals_row = row["Bolnice"].split(",")
            hospitals_list = (
                [Hospital.objects.get(name=h.strip()) for h in hospitals_row]
                if hospitals_row[0].strip() != "*"
                else Hospital.objects.all()
            )
            data = {
                "category": cat,
                "name": row["ime usluge"].strip(),
                "price": row["Cena"] if not math.isnan(row["Cena"]) else 0,
            }
            c = Service.objects.create(**data)
            c.hospitals.set(hospitals_list)
            c.save()

    def handle(self, *args, **options):
        path = options["path"]

        hospitals = pd.read_excel(path, sheet_name="Bolnice")
        self.import_hospitals(hospitals)

        categories = pd.read_excel(path, sheet_name="Kategorije")
        self.import_categories(categories)

        services = pd.read_excel(path, sheet_name="Usluge")
        self.import_services(services)
        # for sheet, df in hospitals.items():
        #     full_row = df.iloc[0]
        #     hosp_name = full_row[0]
        #     hospital, _ = Hospital.objects.get_or_create(name=hosp_name)
        #
        #     for row in df.itertuples(index=False):
        #         # check that the row exists
        #         if not isinstance(row[2], str):
        #             continue
        #
        #         cat_name = row[1].split("-")[0].strip()
        #         category, _ = Category.objects.get_or_create(
        #             defaults={"name": cat_name}, name__iexact=cat_name
        #         )
        #         service, _ = Service.objects.get_or_create(
        #             defaults={"name": row[2], "category": category}, name__iexact=row[2]
        #         )
        #         service.hospitals.add(hospital)
        #         service.save()
