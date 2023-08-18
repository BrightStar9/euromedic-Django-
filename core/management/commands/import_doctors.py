import pandas as pd
from django.core.management.base import BaseCommand

from core.models import Hospital, Doctor, Reference


class Command(BaseCommand):
    help = "Migrates doctors data from xls file"

    def add_arguments(self, parser):
        parser.add_argument("path")

    def import_doctors(self, df):
        self.stdout.write("Started doctors migration...")
        for index, row in df.iterrows():
            doctor_data = {
                "full_name": row["full_name"],
                "specialization": row["speciality"].capitalize(),
                "specialization_details": row["speciality 2"]
                if row["speciality 2"]
                else None,
                "biography": row["biography"].capitalize() if row["biography"] else "",
                "gender": row["genders"],
            }
            self.stdout.write(f"[{index}] Importing doctor: {row['full_name']}...")
            doctor = Doctor.objects.create(**doctor_data)
            references = [
                Reference.objects.create(
                    description=ref.strip().capitalize(), doctor=doctor
                )
                for ref in row["references"].split(";")
                if ref and not ref.isspace()
            ]
            doctor.references.set(references)
            try:
                hospital = Hospital.objects.get(name__iexact=row["location"])
            except Hospital.DoesNotExist:
                self.stderr.write(
                    f"Failed to find hospital with name {row['location']} for doctor "
                    f"{row['full_name']}. Please, import manually!"
                )
            else:
                doctor.hospitals.add(hospital)

            doctor.save()
            self.stdout.write(f"Doctor: {str(doctor)} successfully imported!")

    def handle(self, *args, **options):
        path = options["path"]

        df = pd.read_excel(path, sheet_name="Sheet1", skiprows=2)
        df = df.fillna("")
        df = df[df.full_name != ""]
        self.import_doctors(df)
