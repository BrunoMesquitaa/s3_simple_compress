#!/usr/bin/env python


#==================================================================================================#

#Parametros

# caminho ate data e finalizar com /
caminho_projeto = 'Projetos/2021/IMC/HTMLs/ESTUDOS/NOVA_ALIANCA/BOTAFOGO/202103/'

empresa = "teste_bmesquita" # Alinhar o nome da empresa com time de TI
estado = "RJ" # UF do estado
cidade = "Rio_de_Janeiro" # nome normal com acentos e "_" no lugar de espaços
bairro = "Botafogo" # nome normal com acentos e "_" no lugar de espaços
estudo = "fit" # um desses: fit,lite, pro, expert
periodo = "202103" # data do estudo
#==================================================================================================#

#libs
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
for i in ["boto3"]:
    install(i)
import io
import zipfile
import boto3

#funcoes
def copy_s3_to_s3(caminho_projeto,to_s3_folder,from_bucket,extra_args):

    keys = []
    to_keys = []
    paginator = s3_client.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=from_bucket, Prefix=caminho_projeto)

    for response in response_iterator:

        for object_data in response["Contents"]:
            key = object_data['Key']
            to_key = key.replace(caminho_projeto,'')
            to_key = str(to_s3_folder+to_key)
            keys.append(key)
            to_keys.append(to_key)

    for i in range(len(keys)):

        copy_source = {
            'Bucket': from_bucket,
            'Key': keys[i]
        }

        if(not keys[i].endswith('/')):
            bucket = s3_resource.Bucket(to_bucket)
            bucket.copy(copy_source, to_keys[i],extra_args)
            print(to_keys[i])


def download_s3_folder(bucket_name, to_s3_folder):

        lista = list()
        bucket = s3_resource.Bucket(bucket_name)

        for obj in bucket.objects.filter(Prefix=to_s3_folder):
            byte_io = io.BytesIO()
            s3_resource.Object(bucket_name, obj.key).download_fileobj(byte_io)
            tupla_file = (str((obj.key).replace(to_s3_folder, "")),
                        io.BytesIO(byte_io.getvalue()))
            lista.append(tupla_file)

        return lista


def zipping_s3_folder(lista,to_bucket,to_s3_folder,research_name,periodo,extra_args):

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in lista:
            zip_file.writestr(file_name, data.getvalue())
    zip_buffer.seek(0)

    s3_client.upload_fileobj(zip_buffer, to_bucket,
                            str(to_s3_folder+research_name+periodo+'.zip'), extra_args)


#argumentos
from_bucket = 'dev-datazap'
to_bucket = 'entregaveis-datazap'


research_name = str(estado+'_-_'+cidade+'_-_'+bairro+'_'+estudo)
to_s3_folder = str(empresa+'/'+research_name+'/'+ periodo+'/')

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

extra_args = { 'ACL': 'public-read' }


print('Copiando')
copy_s3_to_s3(caminho_projeto,to_s3_folder,from_bucket,extra_args)      

print("Baixando arquivos")  
lista = download_s3_folder(to_bucket, to_s3_folder)
    
print("Compactando")
zipping_s3_folder(lista,to_bucket,to_s3_folder,research_name,periodo,extra_args)

print("FIM")
