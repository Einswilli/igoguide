# Generated by Django 3.2.12 on 2022-09-01 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=250)),
                ('region', models.CharField(max_length=250)),
                ('createdAt', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etablishment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('presentation', models.CharField(max_length=1500)),
                ('address', models.CharField(max_length=500)),
                ('tags', models.CharField(max_length=2000)),
                ('longitude', models.FloatField(default=0.0)),
                ('latitude', models.FloatField(default=0.0)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.city')),
            ],
        ),
        migrations.CreateModel(
            name='EtablishmentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('createdAt', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('createdAt', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('LName', models.CharField(max_length=50)),
                ('FName', models.CharField(max_length=80)),
                ('Email', models.EmailField(max_length=150, unique=True)),
                ('Phone', models.IntegerField()),
                ('Pass', models.CharField(max_length=25)),
                ('Photo', models.ImageField(upload_to='')),
                ('JoinedAt', models.DateField(auto_now_add=True)),
                ('Type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('isActiive', models.BooleanField(default=True)),
                ('activeDuration', models.IntegerField(default=1)),
                ('fee', models.FloatField(default=49.0)),
                ('stopDate', models.DateField()),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('etablishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('facebookName', models.CharField(max_length=500)),
                ('instagramName', models.CharField(max_length=500)),
                ('tweeterName', models.CharField(max_length=500)),
                ('tiktokName', models.CharField(max_length=500)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('etablishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=0.0)),
                ('status', models.CharField(max_length=20)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='')),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('etablishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Favoris',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('etablishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.user')),
            ],
        ),
        migrations.CreateModel(
            name='EtablishmentSubType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishmenttype')),
            ],
        ),
        migrations.AddField(
            model_name='etablishment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.user'),
        ),
        migrations.AddField(
            model_name='etablishment',
            name='subType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishmentsubtype'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=150)),
                ('website', models.CharField(max_length=300)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('etablishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishment')),
            ],
        ),
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('children', models.CharField(max_length=500)),
                ('pets', models.CharField(max_length=500)),
                ('handicaps', models.CharField(max_length=500)),
                ('breakfast', models.CharField(max_length=500)),
                ('difficults', models.CharField(max_length=500)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('etablishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='igoMaster.etablishment')),
            ],
        ),
    ]
