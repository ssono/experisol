# Generated by Django 2.0.6 on 2018-06-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0017_userstats_totalstats'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['-order']},
        ),
        migrations.AddField(
            model_name='section',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
