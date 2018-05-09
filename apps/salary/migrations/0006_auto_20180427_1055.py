# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-27 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0005_auto_20180426_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salaryrecord',
            name='extrainfo',
            field=models.TextField(blank=True, default='4月工资记录', null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='salaryrecord',
            name='status',
            field=models.CharField(blank=True, choices=[('UNCOMPELTE', '尚未完成本月工资核算'), ('BASESALARYINITCOMPLETE', '已生成基础工资与福利薪酬'), ('CHECKONWORKATTENDANCECOMPLETE', '完成考勤录入'), ('TOTALSALARYCOMPLETE', '已生成薪酬合计'), ('INSURANCEANDFUNDCOMPELTE', '已经录入五险一金并生成应发薪酬'), ('TAXANDOTHERDEDUCTIONS', '已完成税费及其他扣除项录入生成实发薪酬')], default='UNCOMPELTE', max_length=60, null=True, verbose_name='工资记录状态'),
        ),
    ]
