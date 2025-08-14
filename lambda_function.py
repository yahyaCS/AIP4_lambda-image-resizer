import os
import io
import boto3
from PIL import Image, ImageOps

s3 = boto3.client('s3')

DEST_BUCKET = os.getenv('DEST_BUCKET')  
DEST_PREFIX = os.getenv('DEST_PREFIX', 'resized/')
TARGET_WIDTH = int(os.getenv('TARGET_WIDTH', '800'))
TARGET_HEIGHT = int(os.getenv('TARGET_HEIGHT', '600'))

def lambda_handler(event, context):
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if not key.startswith('originals/'):
            continue

        
        obj = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

        
        img = Image.open(io.BytesIO(obj))
        img = ImageOps.exif_transpose(img)

        
        img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT))
        out = io.BytesIO()
       
        fmt = (img.format or "JPEG").upper()
        if fmt not in ["JPEG", "JPG", "PNG", "WEBP"]:
            fmt = "JPEG"
        img.save(out, format=fmt, quality=85, optimize=True)
        out.seek(0)

        dest_bucket = DEST_BUCKET or bucket
        filename = key.rsplit('/', 1)[-1]
        dest_key = f"{DEST_PREFIX}{filename}"

        s3.put_object(
            Bucket=dest_bucket,
            Key=dest_key,
            Body=out,
            ContentType=f"image/{'jpeg' if fmt=='JPG' else fmt.lower()}"
        )

    return {"status": "ok"}
