import pytest, botocore, boto3
from s3_compress.zipping_s3 import ZippingS3
from unittest.mock import patch

zips3 = ZippingS3()


def test_success_check_credentials():
    zips3.credentials(
        ACCESS_KEY='test',
        SECRET_KEY='test',
        SESSION_TOKEN='us-east-1',
        url='http://localhost:4566',
    )
    assert zips3.__s3_client__
    assert zips3.__s3_resource__
    assert isinstance(zips3.__s3_client__, botocore.client.BaseClient)


@pytest.fixture
def config_s3_localstack():
    zips3.__s3_client__.create_bucket(Bucket='test')
    with open('tests/files/test.jpg', 'rb') as f:
        zips3.__s3_client__.upload_fileobj(f, 'test', 'test.jpg')


def test_s3_download_in_memory(config_s3_localstack):
    list_sp = zips3.s3_download_in_memory('test', '')
    result = list()
    [result.append(i[0]) for i in list_sp]
    assert 'test.jpg' in result
    assert len(result) == 1


def test_zipping_in_s3(config_s3_localstack):
    zips3.zipping_in_s3('test', '', 'zip_name')
    result = list()
    [
        result.append(i.key)
        for i in zips3.__s3_resource__.Bucket('test').objects.all()
    ]
    assert 'zip_name.zip' in result
    assert len(result) == 2
