from django.db import migrations


def add_gender_guardian_if_needed(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            ALTER TABLE home_admissionapplication
            ADD COLUMN IF NOT EXISTS gender varchar(10) NOT NULL DEFAULT ''
        """)
        cursor.execute("""
            ALTER TABLE home_admissionapplication
            ADD COLUMN IF NOT EXISTS guardian_name varchar(150) NOT NULL DEFAULT ''
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0055_add_gender_guardian_to_admission'),
    ]

    operations = [
        migrations.RunPython(
            add_gender_guardian_if_needed,
            migrations.RunPython.noop,
        ),
    ]
