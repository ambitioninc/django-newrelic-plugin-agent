from mock import patch
from django.test import TestCase

from newrelic_plugin_agent.interface import push_value


class InterfaceTest(TestCase):

    @patch('newrelic_plugin_agent.interface.PushMetricValueTask')
    def test_push_value(self, task_mock):
        push_value('foo', 'bar')
        task_mock.return_value.delay.assert_called_once_with('foo', 'bar')
