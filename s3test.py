import boto3
 
file1 = open('e:\\amazon\\RickS3Keys.txt', 'r')
lines = file1.readlines()
key1 = lines[0].strip()
key2 = lines[1].strip()
print(key1)
print(key2)
s3client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id=key1,
         aws_secret_access_key= key2
)
 
# These define the bucket and object to read
bucketname = "bos.rick.finance.data"
file_to_read = "invest.json"
#Create a file object using the bucket and object key. 
fileobj = s3client.get_object(
    Bucket=bucketname,
    Key=file_to_read
    ) 
# open the file object and read it into the variable filedata. 
filedata = fileobj['Body'].read()

# file data will be a binary stream.  We have to decode it 
contents = filedata.decode('utf-8') 

# Once decoded, you can treat the file as plain text if appropriate 
print(contents)
