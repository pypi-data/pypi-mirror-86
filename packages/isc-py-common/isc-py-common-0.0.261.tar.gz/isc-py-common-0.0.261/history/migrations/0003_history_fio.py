# Generated by Django 2.2.6 on 2019-10-17 11:35

from django.db import migrations
import isc_common.fields.name_field


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_history_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='fio',
            field=isc_common.fields.name_field.NameField(blank=True, null=True),
        ),
    ]
