from django.db import migrations


def add_gender_guardian_if_needed(apps, schema_editor):
    from django.db import connection
    existing = [col.name for col in connection.introspection.get_table_description(connection.cursor(), 'home_admissionapplication')]
    with connection.cursor() as cursor:
        if 'gender' not in existing:
            cursor.execute("ALTER TABLE home_admissionapplication ADD COLUMN gender varchar(10) NOT NULL DEFAULT ''")
        if 'guardian_name' not in existing:
            cursor.execute("ALTER TABLE home_admissionapplication ADD COLUMN guardian_name varchar(150) NOT NULL DEFAULT ''")


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
