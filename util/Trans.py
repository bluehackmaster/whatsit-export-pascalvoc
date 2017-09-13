import boto3
# import dropbox
import requests

from . import Config

AWS_ACCESS_KEY = Config.getValue('AWS', 'AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = Config.getValue('AWS', 'AWS_SECRET_ACCESS_KEY')
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def downloadFile(save_path, file_url):
    """ Download file from http url link """

    r = requests.get(file_url)  # create HTTP response object

    with open(save_path, 'wb') as f:
        f.write(r.content)

    return save_path


# def downloadFileFromDropbox(save_path, link):
#     """ Download file from dropbox
#     It is need to get a app access token"""
#
#     dbx = dropbox.Dropbox("Access Token")
#     print(dbx.users_get_current_account())
#
#     return dbx.sharing_get_shared_link_file(url=link, path=save_path)
#

def uploadFileToBucket(bucket, file_path, key):
    """ Upload files to S3 Bucket """
    with open(file_path, 'rb') as data:
        s3.upload_fileobj(data, bucket, key)

def downloadFileFromBucket(bucket, file_path, key ):
    """ Download file from S3 Bucket """
    with open(file_path, 'wb') as data:
        s3.download_fileobj(bucket, key, data)
        return file_path