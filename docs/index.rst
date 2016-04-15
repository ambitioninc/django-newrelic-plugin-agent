Django New Relic Plugin Agent Documentation
===========================================

This project provides an interface for publishing arbitrary metrics to New Relic.

Usage
=====

Configuration
-------------

Register Django settings

.. code-block:: python

    >>> NEWRELIC_PLUGIN_AGENT = {
    ...     # number of milliseconds between retries to obtain lock on metric timeslice
    ...     # lock acquired for atomic metric computation/publication operations
    ...     'TIMESLICE_LOCK_RETRY_DELAY_MS': 1000,
    ...     # license key for newrelic account
    ...     'NEWRELIC_LICENSE_KEY': 'keyboardcat',
    ... }


Set metric push task to run as often as you like. New Relic recommends 60 seconds.

.. code-block:: python

    >>> from djcelery.models import PeriodicTask, IntervalSchedule
    >>> interval_schedule = IntervalSchedule.from_schedule(schedule(timedelta(seconds=60)))
    >>> interval_schedule.save()
    >>> PeriodicTask.object.create(
    ...     name='PushMetricTimeslice', interval=interval_schedule, enabled=True,
    ...     task='newrelic_plugin_agent.tasks.PushMetricTimeslicesTask')


Add a Plugin Component
----------------------

A component can be thought of as an aspect of your application/stack that you want to monitor.

.. code-block:: python

    >>> from newrelic_plugin_agent.models import NewRelicComponent
    >>> # create a component
    >>> component = NewRelicComponent.objects.create(
    ...     name='AccountActivity', guid='com.your_company_name.account_activity')


Adding Metric Values to be Sent to New Relic
--------------------------------------------

Push a metric value by forking an async job to add the value to the metric queue

.. code-block:: python

    >>> from newrelic_plugin_agent.tasks import PushMetricValueTask
    >>> # created a new account, track frequency
    >>> PushMetricValueTask.delay(component, 'AccountsCreated', 1)

