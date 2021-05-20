# API Notes

## CRM API

### CRM Authentication

`POST /token`

**Form Data**

```
username
password
```

**Returns**

```
{
	"access_token": <token>,
	"token_type": "bearer"
}
```

All CRM APIs required a Token retrieved via this **CRM Authentication** endpoint.

Put the retrieved token in **header**` Authorization: Bearer <token>`



### CRM List Customers

`GET /crm/customers`

**Query Params**

```
page: int, default 1
page_count: int, default 20
```



### CRM Get Customer Details

`GET /crm/customers/:customer_id`

**Path Parameters**

```python
customer_id: UUID
```

May return **404** if record not found.



### CRM Upload

`POST /crm/upload`

**POST Body**

```python
customers_file: File
```

**Returns**

Record Count



## Customer API

All Customers API require a valid **Application Token** from the PDA with the application id `ld-s-cityofelyriaidentitypassport`

Put the Application Token in **header**` Authorization: Bearer <token>`



### Get Basic Customer Info

`GET /customer/basic`

Use the contents of the key `id` to show the **QR Code**



### Search for Customers

so that you can claim

`POST /customer/search`

**POST Body**

```python
class CustomerSearch(BaseModel):
    last_name: Optional[str] = ''
    house_number: Optional[str] = ''
    email: Optional[str] = ''
```



### Claim Data

`POST /customer/claim`

**POST Body**

```python
id: UUID
```

Using the **id** returned in the list result of **Search for Customers**

