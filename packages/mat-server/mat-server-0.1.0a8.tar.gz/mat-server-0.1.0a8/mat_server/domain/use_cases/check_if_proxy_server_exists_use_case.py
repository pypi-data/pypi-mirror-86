from mat_server.domain import base_types, repositories


class CheckIfProxyServerExistsUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase):
        self._mat_config_repository = mat_config_repository

    def execute(self) -> bool:
        proxy_host = self._mat_config_repository.get_proxy_host()
        return True if proxy_host else False
