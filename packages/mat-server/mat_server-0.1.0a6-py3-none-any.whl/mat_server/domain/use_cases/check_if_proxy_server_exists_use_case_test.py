from unittest import mock

from mat_server.domain import repositories
from mat_server.domain.use_cases import CheckIfProxyServerExistsUseCase


def test_check_proxy_server_not_exists():
    mat_config_repository = mock.MagicMock(spec=repositories.MatConfigRepositoryBase)
    mat_config_repository.get_proxy_host.return_value = None

    uc = CheckIfProxyServerExistsUseCase(
        mat_config_repository=mat_config_repository,
    )

    assert uc.execute() is False

    mat_config_repository.get_proxy_host.assert_called()


def test_check_proxy_server_exists():
    mat_config_repository = mock.MagicMock(spec=repositories.MatConfigRepositoryBase)
    mat_config_repository.get_proxy_host.return_value = 'proxy_url'

    uc = CheckIfProxyServerExistsUseCase(
        mat_config_repository=mat_config_repository,
    )

    assert uc.execute() is True

    mat_config_repository.get_proxy_host.assert_called()
