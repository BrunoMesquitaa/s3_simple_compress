# Tutorial

{% include "templates/basic.md" %}

---

## Going deeper into each function

## credentials():
The `credentials` method is often used to verify who you are and whether you have permission to access the resources you are requesting. So the method may not be necessary to call if you already have a configured `~/.aws/credentials` or if you have environment variables defined with these names `(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)`.

#### Parameters:
- `ACCESS_KEY` - The access key for your AWS account.
- `SECRET_KEY` - The secret key for your AWS account.
- `SESSION_TOKEN` - The session key for your AWS account. This is only needed when you are using temporary credentials. The `AWS_SECURITY_TOKEN` environment variable can also be used, but is only supported for backwards compatibility purposes. `AWS_SESSION_TOKEN` is supported by multiple AWS SDKs besides python.

!!! tip
    You can find more information on the boto3 documentation by clicking [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)

```py title="credentials.py" linenums="1" 
zips3 = ZippingS3()

zips3.credentials(ACCESS_KEY='test', SECRET_KEY='test', SESSION_TOKEN='us-east-1')

```

---

## s3_download_in_memory():
`s3_download_in_memory` is a method that allows you to download a file directly to the RAM memory of a device, without saving it to a permanent storage. This can save disk space and speed up file transfers.

#### Parameters:
- `bucket_name` - The name of the bucket.
- `prefix` - The prefix is used to find the path/file matches.

#### Return:
`list[tuple[str, io.BytesIO()]]`

A method that returns a list of tuples, where each tuple contains a `string` (name file) and an `io.BytesIO()` object (file binary), is returning information about binary files at runtime, without the need to create temporary physical files. This allows for manipulation of binary data without taking up disk space.

```py title="s3_download_in_memory.py" linenums="1" 
zips3 = ZippingS3()

zips3.s3_download_in_memory('bucket_name', 'prefix')
```

---

## zipping_in_s3():

`zipping_in_s3` is a compression method that compresses one or more files into a single compressed ZIP file and stores it directly in AWS S3 cloud storage service. This way, it is possible to save storage space and reduce file transfer costs by sending only one compressed file instead of several uncompressed files.

#### Parameters:
- `bucket_name` - The name of the bucket .
- `prefix` - The prefix is used to find the path/file matches.
- `zip_name` - zip_name is the name given to the compressed file generated from the compression of one or more files in zip format.
- `files` - It is a list of tuples, where each tuple contains a string and an io.BytesIO() object. When this parameter is used, the s3_download_in_memory() method is not executed, which means that the file is not downloaded from AWS S3. This way, it is possible to send a ZIP file directly from the local machine to S3 without the need to download the file from the cloud. `not required`
- `extra_args` - The extra_args parameter is an optional parameter used in the Boto3 library to send additional arguments for the upload or download operation of files in AWS S3. It allows specifying additional options such as metadata or storage settings that can be passed to the S3 service during the file transfer. `not required`

```py title="zipping_in_s3.py" linenums="1" 
zips3 = ZippingS3()

zips3.zipping_in_s3('bucket_name', 'prefix', 'zip_name', 'files', 'extra_args')
```