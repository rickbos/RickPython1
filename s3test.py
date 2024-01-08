import boto3
 
s3client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIAX2S2J624EE6ML65Q',
         aws_secret_access_key= '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'
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
