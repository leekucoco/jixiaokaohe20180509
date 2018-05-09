# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-04 16:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='年度测评', max_length=18, null=True, verbose_name='年度测评')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '年度测评',
                'verbose_name_plural': '年度测评',
            },
        ),
        migrations.AddField(
            model_name='appraisalprocedure',
            name='evaluateoftheyear',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='procedure_evaluate', to='evaluate.Evaluate', verbose_name='年度测评'),
        ),
        migrations.AddField(
            model_name='evaluateresult',
            name='evaluateoftheyear',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_evaluate', to='evaluate.Evaluate', verbose_name='年度测评'),
        ),
    ]
