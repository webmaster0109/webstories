# Generated by Django 5.1.6 on 2025-07-12 10:40

import story_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("story_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="webstory",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="webstory",
            name="slug",
            field=models.SlugField(
                default=story_app.models.get_short_id,
                editable=False,
                help_text="Unique identifier for the story, auto-generated.",
                max_length=20,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="webstoryslide",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
