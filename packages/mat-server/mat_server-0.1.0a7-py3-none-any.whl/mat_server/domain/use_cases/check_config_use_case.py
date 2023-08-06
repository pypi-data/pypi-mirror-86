from mat_server.domain import base_types, repositories, entities


class CheckConfigUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase):
        self._mat_config_repository = mat_config_repository

    def execute(self) -> entities.ValidationReport:
        validation_report = entities.ValidationReport()

        mat_config = self._mat_config_repository.get_config()
        if not mat_config.server.proxy_url and not mat_config.routes:
            validation_report.add_failed_reason('必須要有 proxy url 或 mock 路由設定')

        return validation_report
