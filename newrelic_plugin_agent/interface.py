from newrelic_plugin_agent.tasks import PushMetricValueTask


def push_value(guid, value):
    return PushMetricValueTask().delay(guid, value)
