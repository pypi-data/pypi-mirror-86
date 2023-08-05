import uuid
from typing import List

from mat_server.domain import base_types, entities, repositories, exceptions, helpers


class GetMockResponseUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase,
                 file_helper: helpers.FileHelperBase,
                 json_helper: helpers.JSONHelperBase):
        self._mat_config_repository = mat_config_repository
        self._file_helper = file_helper
        self._json_helper = json_helper

    def execute(self, request: entities.ClientRequest) -> entities.ServerResponse:
        route_config = self._mat_config_repository.query_route_config(
            path=request.path,
            method=request.method,
            query_string=request.query_string,
        )

        if route_config is None:
            raise exceptions.NotFoundError('找不到對應的 ConfigRoute')

        response_config = route_config.response

        if response_config.file_path and response_config.data:
            raise exceptions.ValidationError('回傳資源衝突')

        if response_config.data:
            file_type = self._guess_data_file(response_config)

            # 如果是 json
            if file_type == 'application/json':
                data = self._json_helper.serialize(response_config.data)
            # 其餘直接編碼
            else:
                data = response_config.data

            if response_config.replace_funcs:
                data = self._transform_data(data, response_config.replace_funcs)

            return entities.ServerResponse(
                raw_body=data.encode(),
                status_code=route_config.status_code,
                headers={
                    'Content-Type': self._guess_data_file(response_config),
                },
            )

        elif response_config.file_path:
            response_file_path = self._file_helper.join_file_paths(
                'mat-data',
                response_config.file_path,
            )

            file_type = self._guess_data_file(response_config)
            raw_body = self._file_helper.read_bytes(response_file_path)

            if response_config.replace_funcs:
                data = raw_body.decode()
                raw_body = self._transform_data(data, response_config.replace_funcs).encode()

            return entities.ServerResponse(
                raw_body=raw_body,
                status_code=route_config.status_code,
                headers={
                    'Content-Type': file_type,
                },
            )

        else:
            raise exceptions.ValidationError('找不到對應的回傳資料')

    def _guess_data_file(self, response: entities.RouteResponseConfig):
        if response.data:
            # 如果是字串型態猜測為網頁
            if isinstance(response.data, str):
                return 'text/html; charset=utf-8'
            # 其餘猜測為 json
            else:
                return 'application/json'
        elif response.file_path:
            response_file_path = self._file_helper.join_file_paths(
                'mat-data',
                response.file_path,
            )

            file_type = self._file_helper.guess_file_type(response_file_path)
            # 如果猜不到就當作網頁
            if file_type is None:
                file_type = 'text/html; charset=utf-8'
            return file_type
        else:  # pragma: no cover
            raise exceptions.ValidationError('資訊不足，無法猜測資料型態')

    def _transform_data(self, data: str, replace_funcs: List) -> str:
        for replace_func in replace_funcs:
            if replace_func == 'uuid_v4':
                data = self._transform_for_uuid_v4_replace_func(data)
        return data

    @staticmethod
    def _transform_for_uuid_v4_replace_func(data: str) -> str:
        for _ in range(data.count('{uuid_v4}')):
            data = data.replace('{uuid_v4}', str(uuid.uuid4()), 1)
        return data
