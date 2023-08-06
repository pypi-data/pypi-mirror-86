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

```python
from importlib import reload
from s3bz.s3bz import S3
```

### set up dummy data

## save object using bz2 compression

```python
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

```python
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = True)
print(('doesnt exist', 'exist')[result])
```

    exist


## load object with bz2 compression

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result[0])
```

    {'ib_prcode': '87509', 'ib_brcode': '1017', 'ib_cf_qty': '890', 'new_ib_vs_stock_cv': '99'}


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

    https://pybz-test.s3-accelerate.amazonaws.com/test.dict?AWSAccessKeyId=AKIAVX4Z5TKDVNE5QZPQ&Signature=cvFQZ68uxnq2ryt6fQkvvj%2B88oQ%3D&Expires=1606301851


### download using signed link

```python
from s3bz.s3bz import Requests
result = Requests.getContentFromUrl(url)
```

## File operations

### save without compression

```python
inputPath = '/tmp/tmpFile.txt'
key = 'tmpFile'
downloadPath = '/tmp/downloadTmpFile.txt'
with open(inputPath , 'w')as f:
  f.write('hello world')
```

```python
S3.saveFile(key =key ,path = inputPath,bucket = bucket)
##test
S3.exist(key,bucket)
```




    True



### load without compression

```python
S3.loadFile(key= key , path = downloadPath, bucket = bucket)
```

```python
##test
with open(downloadPath, 'r') as f:
  print(f.read())
```

    hello world


### delete

```python
result = S3.deleteFile(key, bucket)
## test
S3.exist(key,bucket)
```




    False



## save and load pandas dataframe

```python
### please install in pandas, 
### this is not include in the requirements to minimize the size impact
import pandas as pd
df = pd.DataFrame({'test':[1,2,3,4,5],'test2':[2,3,4,5,6]})
S3.saveDataFrame(bucket,key,df)
S3.loadDataFrame(bucket,key)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>test</th>
      <th>test2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>3</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>4</td>
      <td>5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>5</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>


