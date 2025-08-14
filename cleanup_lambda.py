import boto3

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket_name = 'image-resizer-yahya'  
    bucket = s3.Bucket(bucket_name)

    prefixes = ['originals/', 'resized/']  
    deleted_count = 0

    for prefix in prefixes:
        for obj in bucket.objects.filter(Prefix=prefix):
            obj.delete()
            deleted_count += 1

    return {
        "status": f"Deleted {deleted_count} objects from {prefixes} in {bucket_name}"
    }
