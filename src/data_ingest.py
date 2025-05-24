import argparse, boto3, pathlib, urllib.request, gzip, shutil, os

URL = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.tsv.gz"

def download_file(url, local_path):
    print(f"Downloading {url} → {local_path} ...")
    urllib.request.urlretrieve(url, local_path)

def upload_to_s3(local_path, bucket, key):
    s3 = boto3.client('s3')
    s3.upload_file(local_path, bucket, key)
    print(f"Uploaded to s3://{bucket}/{key}")

def main(bucket, raw_path):
    raw_path = pathlib.Path(raw_path)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    download_file(URL, raw_path)
    if bucket != "local":
        upload_to_s3(str(raw_path), bucket, f"openfood/{raw_path.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', default="local",
                        help="S3 bucket name or 'local' to skip upload")
    parser.add_argument('--raw_path', default="data/raw.tsv.gz")
    args = parser.parse_args()
    main(args.bucket, args.raw_path)