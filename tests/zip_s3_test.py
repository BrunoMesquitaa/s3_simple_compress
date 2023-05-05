import pytest, botocore
from s3_compress.zipping_s3 import ZippingS3


zips3 = ZippingS3()


def test_check_no_credentials():
    assert zips3.__s3_client__
    assert zips3.__s3_resource__


def test_check_no_access():
    error = 'Unable to locate credentials'
    try:
        zips3.s3_download_in_memory('test', '')
    except Exception as e:
        assert str(e) == error


def test_check_credentials():
    zips3.credentials(
        ACCESS_KEY='test',
        SECRET_KEY='test',
        SESSION_TOKEN='us-east-1',
        url='http://localhost:4566',
    )
    assert zips3.__s3_client__
    assert zips3.__s3_resource__
    assert isinstance(zips3.__s3_client__, botocore.client.BaseClient)


def test_s3_download_in_memory_NoSuchBucket():
    error = 'An error occurred (NoSuchBucket) when calling the ListObjects operation: The specified bucket does not exist'
    try:
        zips3.s3_download_in_memory('test', '')
    except Exception as e:
        assert str(e) == error


@pytest.fixture
def create_bucket_localstack():
    zips3.__s3_client__.create_bucket(Bucket='test')


def test_s3_download_in_memory_NoSuchFile(create_bucket_localstack):
    result = zips3.s3_download_in_memory('test', 'test')
    assert not result


def test_zipping_in_s3_NoSuchFile(create_bucket_localstack):
    error = 'File or directory is requested but doesn’t exist'
    try:
        zips3.zipping_in_s3('test', 'test', 'zip_name')
    except Exception as e:
        assert str(e) == error


@pytest.fixture
def upload_file_localstack():
    with open('tests/files/test.jpg', 'rb') as f:
        zips3.__s3_client__.upload_fileobj(f, 'test', 'test.jpg')


def test_s3_download_in_memory(
    create_bucket_localstack, upload_file_localstack
):
    list_sp = zips3.s3_download_in_memory('test', '')
    result = list()
    [result.append(i[0]) for i in list_sp]
    assert 'test.jpg' in result
    assert len(result) == 1


def test_zipping_in_s3(create_bucket_localstack, upload_file_localstack):
    zips3.zipping_in_s3('test', '', 'zip_name')
    result = list()
    [
        result.append(i.key)
        for i in zips3.__s3_resource__.Bucket('test').objects.all()
    ]
    assert 'zip_name.zip' in result
    assert len(result) == 2
