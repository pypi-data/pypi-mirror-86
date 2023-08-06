import pickle
from typing import Any

from robinhood_commons.util.aws_utils import get_boto_resource

SERVICE_NAME: str = 's3'
BUCKET_NAME: str = 'robinhood-day-trader'
UTF: str = 'utf-8'


class S3Utils:

    @classmethod
    def client(cls):
        return get_boto_resource(name=SERVICE_NAME)

    @classmethod
    def get_bucket(cls):
        return cls.client().Bucket(BUCKET_NAME)

    @classmethod
    def get_s3_file(cls, path: str):
        return pickle.loads(cls.client().Object(BUCKET_NAME, path).get()['Body'].read())

    @classmethod
    def upload_s3_file(cls, path: str, data: Any) -> None:
        cls.client().put_object(Key=path, Body=pickle.dumps(data))


def main():
    S3Utils.upload_s3_file(path='stocks.json',
                           data=["AAPL", "FRAF", "IPI", "NLOK", "WHR", "FB", "BIIB", "PINS", "DRRX", "IDN"])

    print(S3Utils.get_s3_file(path='stocks.json'))


if __name__ == '__main__':
    main()
