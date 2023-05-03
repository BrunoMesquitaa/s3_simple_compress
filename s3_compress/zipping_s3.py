
import io
import zipfile
import boto3



def credentials(ACCESS_KEY:str = None, SECRET_KEY:str = None, SESSION_TOKEN:str = None) -> list:
    s3_client = boto3.client('s3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN)

    s3_resource = boto3.resource('s3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN)
    
    global __s3_client__
    global __s3_resource__

    __s3_client__ = s3_client
    __s3_resource__ = s3_resource

def s3_download_in_memory(bucket_name:str, prefix:str) -> list:

        files = list()
        bucket = __s3_resource__.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=prefix):
            byte_io = io.BytesIO()
            __s3_resource__.Object(bucket_name, obj.key).download_fileobj(byte_io)
            tupla_file = (str((obj.key).replace(prefix, "")),
                        io.BytesIO(byte_io.getvalue()))
            files.append(tupla_file)

        return files


def zipping_in_s3(files:list, bucket:str ,prefix:str, zip_name:str ,extra_args:dict = None):

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in files:
            zip_file.writestr(file_name, data.getvalue())
    zip_buffer.seek(0)

    __s3_client__.upload_fileobj(zip_buffer, bucket, str(prefix+zip_name+'.zip'), extra_args)


#argumentos
bucket = 'album-mesquita'
zip_name = 'zip_name'
prefix = 'd2ae961cf5714cf2a37473b84cd0bfbd'

credentials()

print("Baixando arquivos")  
files = s3_download_in_memory(bucket, prefix)

print("Compactando")
zipping_in_s3(files,bucket,prefix,zip_name)

print("FIM")
