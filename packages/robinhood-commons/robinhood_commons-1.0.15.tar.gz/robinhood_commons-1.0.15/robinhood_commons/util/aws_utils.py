from __future__ import annotations

import boto3
from boto3.session import Session

REGION_NAME: str = 'us-west-2'


class AwsUtils:

    @classmethod
    def get_boto_resource(cls, name: str = 's3'):
        return boto3.resource(service_name=name)

    @classmethod
    def _open_boto_session(cls) -> Session:
        return boto3.session.Session()

    @classmethod
    def get_boto_client(cls, name: str = 'secretsmanager', region_name: str = REGION_NAME):
        return AwsUtils._open_boto_session().client(service_name=name, region_name=region_name)


if __name__ == '__main__':
    print(AwsUtils.get_boto_client())
