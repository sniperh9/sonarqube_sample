import boto3

# 하드코딩된 AWS API 키
aws_access_key_id = "AKIAQMBDQXYDM7CB4TE6"
aws_secret_access_key = "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"
region_name = "us-east-1"  # 사용하려는 AWS 리전

# boto3 클라이언트 생성 (하드코딩된 API 키 사용)
s3_client = boto3.client(
    "s3", 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key, 
    region_name=region_name
)

# S3 버킷 목록 가져오기
response = s3_client.list_buckets()

# 결과 출력
print("S3 버킷 목록:")
for bucket in response['Buckets']:
    print(f"- {bucket['Name']}")