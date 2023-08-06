from unittest import mock

from mat_server.infrastructure.helpers import JSONHelper


def test_serialize():
    json_module = mock.MagicMock()
    json_module.dumps.return_value = 'serialized_data'

    json_helper = JSONHelper(
        json_module=json_module,
    )

    assert json_helper.serialize('data') == json_module.dumps.return_value
    json_module.dumps.assert_called_with('data')
