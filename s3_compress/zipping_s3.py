import io
import zipfile
import boto3
from rich import print
from rich.progress import Progress
from rich.console import Console


class ZippingS3:
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
            bucket_name: The bucket name of the bucket containing the object.
            prefix: Limits the response to keys that begin with the specified prefix.
        Returns:
            Return a list of tuples with the file name and a binary file.
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

        print('[green]\nStart Download :rocket:')
        with Progress() as progress:
            files = list()
            bucket = self.__s3_resource__.Bucket(bucket_name)
            objects = bucket.objects.filter(Prefix=prefix)
            task = progress.add_task(
                '[green]Downloading...', total=len(list(objects))
            )

            for obj in objects:
                byte_io = io.BytesIO()
                self.__s3_resource__.Object(
                    bucket_name, obj.key
                ).download_fileobj(byte_io)
                tupla_file = (
                    str((obj.key).replace(prefix, '')),
                    io.BytesIO(byte_io.getvalue()),
                )
                files.append(tupla_file)
                progress.update(task, advance=1)
        print('[green]Finish Download :ok_hand:\n')
        return files

    def zipping_in_s3(
        self,
        bucket_name: str,
        prefix: str,
        zip_name: str,
        # files: list = None,
        extra_args: dict = None,
    ) -> None:

        """
        Parameters:
            files: list of binary files from s3_download_in_memory()
            bucket_name: The bucket name of the bucket containing the object.
            prefix: Limits the response to keys that begin with the specified prefix.
            zip_name: Name of Zip file.
            extra_args: Extra arguments that may be passed to the client operation. For allowed upload arguments see boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS.
        Returns:
            Return None
        Examples:
            >>> zipping_in_s3('files', 'bucket_name', 'prefix', 'zip_name')
        """

        files = self.s3_download_in_memory(bucket_name, prefix)

        print('[green]Start zip :package:')
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
        print('[green]Finish zip :ok_hand:\n')

        print('[green]All Rigth :tada::tada::tada:')
