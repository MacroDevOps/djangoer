# Generated by Django 3.2.14 on 2022-07-20 06:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_celery_beat.validators
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClockedSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clocked_time', models.DateTimeField(help_text='Run the task at clocked time', verbose_name='Clock Time')),
            ],
            options={
                'verbose_name': 'clocked',
                'verbose_name_plural': '定时时间',
                'ordering': ['clocked_time'],
            },
        ),
        migrations.CreateModel(
            name='CrontabSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.CharField(default='*', help_text='一小时的分钟. 使用 "*" 表示 "每一分钟". (Example: "0,30")', max_length=240, validators=[django_celery_beat.validators.minute_validator], verbose_name='分钟')),
                ('hour', models.CharField(default='*', help_text='一天的cron小时. 使用 "*" 表示 "每一小时". . (Example: "8,20")', max_length=96, validators=[django_celery_beat.validators.hour_validator], verbose_name='一天的小时')),
                ('day_of_week', models.CharField(default='*', help_text='一个周的cron日. 使用 "*" 表示 "当月每一天". (Example: "0,5")', max_length=64, validators=[django_celery_beat.validators.day_of_week_validator], verbose_name='一周的第几天')),
                ('day_of_month', models.CharField(default='*', help_text='一个月的cron日. 使用 "*" 表示 "当月每一天". (Example: "1,15")', max_length=124, validators=[django_celery_beat.validators.day_of_month_validator], verbose_name='一个月的第几天')),
                ('month_of_year', models.CharField(default='*', help_text='一年的Cron月运行。用“*”代替“all”。(Example: "0,6")', max_length=64, validators=[django_celery_beat.validators.month_of_year_validator], verbose_name='一年的第几个月')),
                ('timezone', timezone_field.fields.TimeZoneField(default='Asia/shanghai', help_text='要运行Cron计划的时区。默认是 Asia/shanghai.', verbose_name='Cron 时区')),
            ],
            options={
                'verbose_name': 'crontabs',
                'verbose_name_plural': 'crontab时间',
                'ordering': ['month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute', 'timezone'],
            },
        ),
        migrations.CreateModel(
            name='IntervalSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('every', models.IntegerField(help_text='再次运行任务之前等待的间隔时长', validators=[django.core.validators.MinValueValidator(1)], verbose_name='时长')),
                ('period', models.CharField(choices=[('days', '日'), ('hours', '小时'), ('minutes', '分钟'), ('seconds', '秒'), ('microseconds', '微秒')], help_text='时间单位(例如:天)', max_length=24, verbose_name='时间单位')),
            ],
            options={
                'verbose_name': '固定间隔时间',
                'verbose_name_plural': '固定间隔时间',
                'ordering': ['period', 'every'],
            },
        ),
        migrations.CreateModel(
            name='PeriodicTasks',
            fields=[
                ('ident', models.SmallIntegerField(default=1, primary_key=True, serialize=False, unique=True)),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SolarSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('dawn_astronomical', 'Astronomical dawn'), ('dawn_civil', 'Civil dawn'), ('dawn_nautical', 'Nautical dawn'), ('dusk_astronomical', 'Astronomical dusk'), ('dusk_civil', 'Civil dusk'), ('dusk_nautical', 'Nautical dusk'), ('solar_noon', 'Solar noon'), ('sunrise', 'Sunrise'), ('sunset', 'Sunset')], help_text='任务运行时的太阳事件类型', max_length=24, verbose_name='Solar Event')),
                ('latitude', models.DecimalField(decimal_places=6, help_text='当事件在该纬度发生时运行任务', max_digits=9, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=6, help_text='当事件在此经度发生时运行任务', max_digits=9, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Longitude')),
            ],
            options={
                'verbose_name': 'solar event',
                'verbose_name_plural': '公共时间',
                'ordering': ('event', 'latitude', 'longitude'),
                'unique_together': {('event', 'latitude', 'longitude')},
            },
        ),
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='简短的标记任务', max_length=200, unique=True, verbose_name='任务名')),
                ('task', models.CharField(help_text='应该运行的celery任务的名称.  (Example: "proj.tasks.import_contacts")', max_length=200, verbose_name='任务名')),
                ('args', models.TextField(blank=True, default='[]', help_text='JSON encoded positional arguments (Example: ["arg1", "arg2"])', verbose_name='位置参数')),
                ('kwargs', models.TextField(blank=True, default='{}', help_text='JSON encoded keyword arguments (Example: {"argument": "value"})', verbose_name='关键字参数')),
                ('queue', models.CharField(blank=True, default=None, help_text='Queue defined in CELERY_TASK_QUEUES. Leave None for default queuing.', max_length=200, null=True, verbose_name='覆盖队列')),
                ('exchange', models.CharField(blank=True, default=None, help_text='Override Exchange for low-level AMQP routing', max_length=200, null=True, verbose_name='Exchange')),
                ('routing_key', models.CharField(blank=True, default=None, help_text='Override Routing Key for low-level AMQP routing', max_length=200, null=True, verbose_name='Routing Key')),
                ('headers', models.TextField(blank=True, default='{}', help_text='JSON encoded message headers for the AMQP message.', verbose_name='AMQP Message Headers')),
                ('priority', models.PositiveIntegerField(blank=True, default=None, help_text='Priority Number between 0 and 255. Supported by: RabbitMQ, Redis (priority reversed, 0 is highest).', null=True, validators=[django.core.validators.MaxValueValidator(255)], verbose_name='优先级')),
                ('expires', models.DateTimeField(blank=True, help_text='日期时间，之后将不再触发任务运行', null=True, verbose_name='取消时间')),
                ('expire_seconds', models.PositiveIntegerField(blank=True, help_text='以秒为单位使timedelta过期', null=True, verbose_name='Expires timedelta with seconds')),
                ('one_off', models.BooleanField(default=False, help_text='如果为True，则计划将只运行该任务一次', verbose_name='任务只运行一次')),
                ('start_time', models.DateTimeField(blank=True, help_text='“时间表开始的日期触发任务运行', null=True, verbose_name='开始日期')),
                ('enabled', models.BooleanField(default=True, help_text='设置为False以禁用计划', verbose_name='Enabled')),
                ('last_run_at', models.DateTimeField(blank=True, editable=False, help_text='schedule最后一次触发任务运行的日期时间,重置为None如果启用设置为False.', null=True, verbose_name='Last Run Datetime')),
                ('total_run_count', models.PositiveIntegerField(default=0, editable=False, help_text='不停地计算日程安排的次数触发了这个任务', verbose_name='运行总数')),
                ('date_changed', models.DateTimeField(auto_now=True, help_text='最后一次修改这个定时任务的日期时间', verbose_name='最后修改')),
                ('description', models.TextField(blank=True, help_text='对该周期任务详细信息的详细说明', verbose_name='详情')),
                ('clocked', models.ForeignKey(blank=True, help_text='运行任务的计时时间表, 时间为固定', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.clockedschedule', verbose_name='定时时间')),
                ('crontab', models.ForeignKey(blank=True, help_text='Crontab 格式的时间设置 如: */15 * * * *', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.crontabschedule', verbose_name='Crontab时间')),
                ('interval', models.ForeignKey(blank=True, help_text='固定时间间隔，如: 15s执行一次。', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.intervalschedule', verbose_name='固定间隔时间')),
                ('solar', models.ForeignKey(blank=True, help_text='公共时间表述, 如一周的第几天，一个月的第几天', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.solarschedule', verbose_name='公共时间')),
            ],
            options={
                'verbose_name': '周期性任务',
                'verbose_name_plural': '周期性任务',
            },
        ),
    ]
