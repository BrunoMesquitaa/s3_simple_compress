import io
import zipfile
import boto3
from rich.progress import Progress
from rich.console import Console


class ZippingS3:

    __s3_client__ = boto3.client('s3')

    __s3_resource__ = boto3.resource('s3')

    console = Console()

    def credentials(
        self,
        ACCESS_KEY: str = None,
        SECRET_KEY: str = None,
        SESSION_TOKEN: str = None,
        url: str = None,
    ) -> None:

        """
        Parameters:
            ACCESS_KEY: AWS_ACCESS_KEY_ID - The access key for your AWS account.
            SECRET_KEY: AWS_SECRET_ACCESS_KEY - The secret key for your AWS account.
            SESSION_TOKEN: AWS_SESSION_TOKEN - The session key for your AWS account. This is only needed when you are using temporary credentials. The AWS_SECURITY_TOKEN environment variable can also be used, but is only supported for backwards compatibility purposes. AWS_SESSION_TOKEN is supported by multiple AWS SDKs besides python.
        Returns:
            Return None, all variable will be sets as global variable.
        Examples:
            >>> credentials('ACCESS_KEY', 'SECRET_KEY', 'SESSION_TOKEN')
        """

        self.__s3_client__ = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            endpoint_url=url,
        )

        self.__s3_resource__ = boto3.resource(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            endpoint_url=url,
        )

    def s3_download_in_memory(
        self, bucket_name: str, prefix: str
    ) -> list[tuple[str, io.BytesIO()]]:

        """
        Parameters:
            bucket_name: The name of the bucket.
            prefix: The prefix is used to find the path/file matches.
        Returns:
            A method that returns a list of tuples, where each tuple contains a `string` (name file) and an `io.BytesIO()` object (file binary), is returning information about binary files at runtime, without the need to create temporary physical files. This allows for manipulation of binary data without taking up disk space.
        Examples:
            >>> s3_download_in_memory('bucket_name', 'prefix')
            [
                ('1.jpeg', <_io.BytesIO object at 0x7fb7ec9825c0>),
                ('2.jpeg', <_io.BytesIO object at 0x7fb7ef08d9e0>),
                ('3.jpeg', <_io.BytesIO object at 0x7fb7ec9bff60>),
                ('4.jpeg', <_io.BytesIO object at 0x7fb7ed38fec0>),
                ('5.jpeg', <_io.BytesIO object at 0x7fb7ec983790>),
            ]
        """

        self.console.print('[green]\nStart Download :rocket:')
        with Progress() as progress:
            files = list()
            bucket = self.__s3_resource__.Bucket(bucket_name)
            objects = bucket.objects.filter(Prefix=prefix)
            task = progress.add_task(
                '[green]Downloading...', total=len(list(objects))
            )

            for obj in objects:

                name = str(
                    (obj.key).replace(
                        str('/'.join(prefix.split('/')[:-1])), ''
                    )
                )
                if name.startswith('/'):
                    name = name[1:]

                byte_io = io.BytesIO()
                self.__s3_resource__.Object(
                    bucket_name, obj.key
                ).download_fileobj(byte_io)
                tupla_file = (
                    name,
                    io.BytesIO(byte_io.getvalue()),
                )
                files.append(tupla_file)
                progress.update(task, advance=1)
        self.console.print('[green]Finish Download :ok_hand:\n')
        return files

    def zipping_in_s3(
        self,
        bucket_name: str,
        prefix: str,
        zip_name: str,
        files: list = None,
        extra_args: dict = None,
    ) -> None:

        """
        Parameters:
            bucket_name: The name of the bucket .
            prefix: The prefix is used to find the path/file matches.
            zip_name: zip_name is the name given to the compressed file generated from the compression of one or more files in zip format.
            files: It is a list of tuples, where each tuple contains a string and an io.BytesIO() object. When this parameter is used, the s3_download_in_memory() method is not executed, which means that the file is not downloaded from AWS S3. This way, it is possible to send a ZIP file directly from the local machine to S3 without the need to download the file from the cloud.
            extra_args: The extra_args parameter is an optional parameter used in the Boto3 library to send additional arguments for the upload or download operation of files in AWS S3. It allows specifying additional options such as metadata or storage settings that can be passed to the S3 service during the file transfer.
        Returns:
            Return None
        Examples:
            >>> zipping_in_s3('bucket_name', 'prefix', 'zip_name')
        """
        if not files:
            files = self.s3_download_in_memory(bucket_name, prefix)
            if len(files) == 0:
                raise FileNotFoundError(
                    'File or directory is requested but doesn’t exist'
                )
        try:
            for f in files:
                if not (
                    type(f) is tuple
                    and type(f[0]) is str
                    and type(f[1]) is io.BytesIO
                ):
                    raise TypeError(
                        'Object has inappropriate type, accepted format (list[tuple[str, io.BytesIO()]])'
                    )
        except:
            raise TypeError(
                'Object has inappropriate type, accepted format (list[tuple[str, io.BytesIO()]])'
            )

        if '/' in prefix:
            prefix = '/'.join(prefix.split('/')[:-1]) + '/'
        else:
            prefix = ''

        self.console.print('[green]Start zip :package:')
        with self.console.status('Initial status ') as status:

            status.update(
                '[green]zipping...',
                spinner='bouncingBall',
                spinner_style='green',
            )
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(
                zip_buffer, 'a', zipfile.ZIP_DEFLATED, False
            ) as zip_file:
                for file_name, data in files:
                    zip_file.writestr(file_name, data.getvalue())
            zip_buffer.seek(0)

            status.update(
                '[green]uploading...',
                spinner='bouncingBall',
                spinner_style='green',
            )
            self.__s3_client__.upload_fileobj(
                zip_buffer,
                bucket_name,
                str(prefix + zip_name + '.zip'),
                extra_args,
            )
        self.console.print('[green]Finish zip :ok_hand:\n')

        self.console.print('[green]All Rigth :tada::tada::tada:')
