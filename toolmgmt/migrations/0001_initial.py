# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IpSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_start', models.GenericIPAddressField()),
                ('ip_end', models.GenericIPAddressField()),
                ('start_int', models.BigIntegerField(default=0)),
                ('end_int', models.BigIntegerField(default=0)),
                ('address', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
    ]
