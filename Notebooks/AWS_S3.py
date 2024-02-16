import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_to_s3(file_paths, bucket_name):
   


    # Retrieve AWS credentials from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")

    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    uploaded_files = []

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        s3_key = f"data/{file_name}"  # You can change the S3 key structure as needed
        s3.upload_file(file_path, bucket_name, s3_key)
        s3_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_key}"
        uploaded_files.append(s3_url)

    return uploaded_files

if __name__ == "__main__":
    # Example file paths
    csv_file_path = "Team05.csv"
    grobid_text_file_paths = ["Grobid_RR_2024_LevelI_combined.txt","Grobid_RR_2024_LevelII_combined.txt","Grobid_RR_2024_LevelIII_combined.txt"]
    pypdf_text_file_paths = ["PyPDF_2024_l1_combined.txt","PyPDF_2024_l2_combined.txt","PyPDF_2024_l3_combined.txt"]
    bucket_name = "cfa-assignment2"  # Replace 'your_bucket_name' with your desired bucket name

    # Combine all file paths
    file_paths = [csv_file_path] + grobid_text_file_paths + pypdf_text_file_paths

    # Upload files to S3
    uploaded_files = upload_to_s3(file_paths, bucket_name)

    # Print uploaded file URLs
    for file_url in uploaded_files:
        print("Uploaded file URL:", file_url)
