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


Adding Metric Values to be Sent to New Relic
--------------------------------------------

Pushing a metric value through the interface will fork an async job to add the value to the metric queue

.. code-block:: python

    >>> from newrelic_plugin_agent.interface import push_value
    >>> push_value('AccountsCreated', 1) # created a new account, track frequency
