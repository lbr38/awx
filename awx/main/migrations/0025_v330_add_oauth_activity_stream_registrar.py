# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 19:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2_provider
import re

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_v330_create_user_session_membership'),
    ]
    run_before = [
        # As of this migration, OAuth2Application and OAuth2AccessToken are models in main app
        # Grant and RefreshToken models are still in the oauth2_provider app and reference
        # the app and token models, so these must be created before the oauth2_provider models
        ('oauth2_provider', '0001_initial')
    ]

    operations = [

        migrations.CreateModel(
            name='OAuth2Application',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('client_id', models.CharField(db_index=True, default=oauth2_provider.generators.generate_client_id, max_length=100, unique=True)),
                ('redirect_uris', models.TextField(blank=True, help_text='Allowed URIs list, space separated', validators=[oauth2_provider.validators.validate_uris])),
                ('client_type', models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], max_length=32)),
                ('authorization_grant_type', models.CharField(choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')], max_length=32)),
                ('client_secret', models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, default=b'')),
                ('logo_data', models.TextField(default=b'', editable=False, validators=[django.core.validators.RegexValidator(re.compile(b'.*'))])),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_oauth2application', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'application',
            },
        ),
        migrations.CreateModel(
            name='OAuth2AccessToken',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('expires', models.DateTimeField()),
                ('scope', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(blank=True, default=b'', max_length=200)),
                ('last_used', models.DateTimeField(default=None, editable=False, null=True)),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_oauth2accesstoken', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'access token',
            },
        ),
        migrations.AddField(
            model_name='activitystream',
            name='o_auth2_access_token',
            field=models.ManyToManyField(to='main.OAuth2AccessToken', blank=True, related_name='main_o_auth2_accesstoken'),
        ),
        migrations.AddField(
            model_name='activitystream',
            name='o_auth2_application',
            field=models.ManyToManyField(to='main.OAuth2Application', blank=True, related_name='main_o_auth2_application'),
        ),

    ]
