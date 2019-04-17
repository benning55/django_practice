# Generated by Django 2.1.7 on 2019-04-17 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_comment'),
    ]

    operations = [
        #migrations.RenameModel(
            #old_name='Choices',
            #new_name='Choice',
        #),
        migrations.AddField(
            model_name='comment',
            name='poll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
