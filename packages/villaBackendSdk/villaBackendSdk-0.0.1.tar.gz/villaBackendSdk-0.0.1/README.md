# SDK for villa e-commerce Backend



postman Terminal [file ](https://github.com/thanakijwanavit/villaEcommerceBackend/blob/master/backend/basket/ecommerceBackend.postman_collection.json)


## Full Documentation  [Here](https://documenter.getpostman.com/view/7814112/TVes6Rfv)

## How to use

1. Create a bucket
2. fill in the products
3. modify the quantity and update products
4. trigger conversion to cart referencing a bucket

# SDK docs

```
from villaBackendSdk.basket import BasketSdk
```

```
basketSdk = BasketSdk(branch='dev')
```

```
inputDict = {
    "basketId" : "1234",
    "basketName" : "1234",
    "ownerId" : "1234"
}
basketSdk.create(inputDict)
```




    {'body': '{"result":{"basketId":"1234","creationTime":1605790015.917538,"basketName":"1234","ownerId":"1234","productList":[]},"Metadata":{"ConsumedCapacity":{"TableName":"basket-table-dev","CapacityUnits":3.0}}}',
     'statusCode': 200,
     'headers': {}}



```
inputDict = {
    'basketId': '1234',
    'items': [{'sku':'123','quantity':-123},{'sku':'456','quantity':123}],
  }
basketSdk.add(inputDict)
```




    {'body': '{"basketId":"1234","creationTime":1605790015.917538,"basketName":"1234","ownerId":"1234","productList":[{"sku":"456","quantity":123}]}',
     'statusCode': 200,
     'headers': {}}



```
inputDict = {
    'basketId': '1234',
    'basketName': 'test',
    'ownerId': '1234',
    'items': [{'sku':'123234','quantity':123},{'sku':'456','quantity':123}]
  }
basketSdk.update(inputDict)
```




    {'body': '{"basketId":"1234","creationTime":1605790015.917538,"basketName":"1234","ownerId":"1234","productList":[{"sku":"123234","quantity":123},{"sku":"456","quantity":123}]}',
     'statusCode': 200,
     'headers': {}}



```
inputDict = {
    'basketId': '1234',
  }
basketSdk.get(inputDict)
```




    {'body': '{"basketId":"1234","creationTime":1605790015.917538,"basketName":"1234","ownerId":"1234","productList":[{"sku":"123234","quantity":123},{"sku":"456","quantity":123}]}',
     'statusCode': 200,
     'headers': {}}



```
inputDict = {
    'basketId': '1234'
  }
basketSdk.empty(inputDict)
```




    {'body': '{"basketId":"1234","creationTime":1605790015.917538,"basketName":"1234","ownerId":"1234","productList":[]}',
     'statusCode': 200,
     'headers': {}}



```
inputDict = {
    'basketId': '1234'
  }
basketSdk.remove(inputDict)
```




    {'body': '{"basketDeleted":{"basketId":"1234","creationTime":1605790015.917538,"basketName":"1234","ownerId":"1234","productList":[]}}',
     'statusCode': 200,
     'headers': {}}


