# Generated by Django 5.0.1 on 2024-03-24 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0002_exercisefamily_created_by_exercisefamilysharedwith_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='bodyweight_inclusion_factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
        ),
        migrations.AddField(
            model_name='exercise',
            name='weight_factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name='exercisefamily',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='exerciseset',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AddConstraint(
            model_name='exercise',
            constraint=models.CheckConstraint(check=models.Q(('bodyweight_inclusion_factor__gte', 0)), name='bodyweight_inclusion_factor>=0'),
        ),
        migrations.AddConstraint(
            model_name='exercise',
            constraint=models.CheckConstraint(check=models.Q(('bodyweight_inclusion_factor__lte', 1)), name='bodyweight_inclusion_factor<=0'),
        ),
        migrations.AddConstraint(
            model_name='exercise',
            constraint=models.CheckConstraint(check=models.Q(('weight_factor__gte', 0)), name='weight_factor>=0'),
        ),
    ]
