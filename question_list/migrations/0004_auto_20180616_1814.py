# Generated by Django 2.2.dev20180612192205 on 2018-06-16 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_list', '0003_auto_20180616_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]