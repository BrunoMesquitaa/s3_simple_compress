# S3 Simple Compress ZIP
## Documentation for AWS S3 In-Memory File Compression (zip) Program

[![Python tests](https://github.com/BrunoMesquitaa/s3_simple_compress/actions/workflows/pytest.yml/badge.svg)](https://github.com/BrunoMesquitaa/s3_simple_compress/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/github/BrunoMesquitaa/s3_simple_compress/branch/main/graph/badge.svg?token=9J8EV3D4T3)](https://codecov.io/github/BrunoMesquitaa/s3_simple_compress)
[![Documentation Status](https://readthedocs.org/projects/s3-simple-compress/badge/?version=latest)](https://s3-simple-compress.readthedocs.io/en/latest/?badge=latest)

## Overview

The AWS S3 file compression (zip) program is a tool that allows users to compress one or more files stored in S3 into a single zip file all in memory without the need to download to your Hard Disk. This can be useful for reducing file sizes and saving storage costs.

## Requirements

Before using the AWS S3 file compression (zip) program, you'll need to have the following:
```
- An AWS account
- Access to the AWS S3 service
- Basic knowledge of command line and AWS
```

---

## Installation

### How to install the project

#### Overview

The AWS S3 file compression (zip) program is a tool that allows users to compress one or more files stored in S3 into a single zip file all in memory without the need to download to your Hard Disk. This can be useful for reducing file sizes and saving storage costs.
Requirements

Before using the AWS S3 file compression (zip) program, you'll need to have the following:

#### Bash

An AWS account
Access to the AWS S3 service
Basic knowledge of command line and AWS

Installation
How to install the project

For installation of the project's CLI, we recommend using poetry to install:

```console
poetry add s3-simple-compress
```

Although this is only a recommendation! You can also install the project with your preferred package manager, such as pip:

```console
pip install s3-simple-compress
```

---

## How to use the program

To use the AWS S3 file compression (zip) program, follow the steps below:
```
- First, we need to import our package
- Then, instantiate the class
- We may or may not need to call the `credentials` method, depending on whether `~/.aws/credentials` already exists or not
- Finally, we just need to call the `zipping_in_s3` method
```
The program will compress the specified files and save the compressed zip file in the specified S3 bucket.

## Code Example

```py title="example.py" linenums="1" 
from s3_compress.zipping_s3 import ZippingS3

zips3 = ZippingS3()

zips3.credentials(
        ACCESS_KEY='test',
        SECRET_KEY='test',
        SESSION_TOKEN='us-east-1'
    )

zips3.zipping_in_s3('test', '', 'zip_name')
```

Here's a Python code example that implements the AWS S3 file compression (zip) program's functionality 100% in memory.