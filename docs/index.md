# S3 Simple Compress
## Documentação do programa de compactação (zip) de arquivos no S3 da AWS

{% include "templates/cards.html" %}

## Visão geral

O programa de compactação (zip) de arquivos no S3 da AWS é uma ferramenta que permite aos usuários compactar um ou mais arquivos armazenados no S3 em um único arquivo zip tudo isso em memoria sem a necessidade de ter que baixar no seu Hard Disk. Isso pode ser útil para reduzir o tamanho dos arquivos e economizar custos de armazenamento.

## Requisitos

Antes de começar a usar o programa de compactação (zip) de arquivos no S3 da AWS, você precisará ter o seguinte:

    Uma conta da AWS
    Acesso ao serviço S3 da AWS
    Conhecimento básico sobre a linha de comando e AWS

## Instalação

{% include "templates/install.md" %}

## Como usar o programa

Para usar o programa de compactação (zip) de arquivos no S3 da AWS, siga as etapas abaixo:

    Abra o terminal ou prompt de comando e navegue até a pasta onde o programa foi instalado.
    Execute o comando python main.py para iniciar o programa.
    Quando solicitado, forneça as seguintes informações:
        O nome do bucket S3 onde estão localizados os arquivos a serem compactados.
        Uma lista de chaves de objetos S3 que serão compactados. Cada chave representa um arquivo individual no bucket.
        O nome do arquivo zip resultante da compactação.
    Pressione Enter para iniciar a compactação.

O programa irá compactar os arquivos especificados e salvar o arquivo zip compactado no bucket S3 especificado.

## Exemplo de código

Aqui está um exemplo de código Python que implementa a funcionalidade de compactação (zip) de arquivos no S3 da AWS: