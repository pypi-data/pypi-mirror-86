# S3Bz
> save and load dictionary to s3 using bz compression


## Install

`pip install s3bz`

## How to use

### Create a bucket and make sure that it has transfer acceleration enabled
#### create a buket
`aws s3 mb s3://<bucketname>`
#### put transfer acceleration
`aws s3api put-bucket-accelerate-configuration --bucket <bucketname> --accelerate-configuration Status=Enabled`

First, import the s3 module

## import package

```
from importlib import reload
from s3bz.s3bz import S3
```

### set up dummy data

## save object using bz2 compression

```
result = S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True)
print(('failed', 'success')[result])
```

    success


## check if an object exist

```
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = True)
print(('doesnt exist', 'exist')[result])
```

    exist


## load object with bz2 compression

```
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result[0])
```

    {'ib_prcode': '58813', 'ib_brcode': '1029', 'ib_cf_qty': '314', 'new_ib_vs_stock_cv': '273'}


## presign download object

```
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

    https://pybz-test.s3-accelerate.amazonaws.com/test.dict?AWSAccessKeyId=AKIAVX4Z5TKDVNE5QZPQ&Signature=bv5NIDX5QCyTYO8X%2Buoy%2FxogDBk%3D&Expires=1605358067


### download using signed link

```
from s3bz.s3bz import Requests
result = Requests.getContentFromUrl(url)
```

## File operations

### save without compression

```
inputPath = '/tmp/tmpFile.txt'
key = 'tmpFile'
downloadPath = '/tmp/downloadTmpFile.txt'
with open(inputPath , 'w')as f:
  f.write('hello world')
```

```
S3.saveFile(key =key ,path = inputPath,bucket = bucket)
##test
S3.exist(key,bucket)
```




    True



### load without compression

```
S3.loadFile(key= key , path = downloadPath, bucket = bucket)
```

```
##test
with open(downloadPath, 'r') as f:
  print(f.read())
```

    hello world


### delete

```
result = S3.deleteFile(key, bucket)
## test
S3.exist(key,bucket)
```




    False



## save and load pandas dataframe

```
import pandas as pd
df = pd.DataFrame({'test':[1,2,3,4,5],'test2':[2,3,4,5,6]})
S3.saveDataFrame(bucket,key,df)
S3.loadDataFrame(bucket,key)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-38-293a2ab02dd8> in <module>
          1 import pandas as pd
          2 df = pd.DataFrame({'test':[1,2,3,4,5],'test2':[2,3,4,5,6]})
    ----> 3 S3.saveDataFrame(bucket,key,df)
          4 S3.loadDataFrame(bucket,key)


    AttributeError: type object 'S3' has no attribute 'saveDataFrame'

