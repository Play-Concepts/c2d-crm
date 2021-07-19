# The DataPassport API

## Prerequisites
1. `docker` environment
2. `docker-compose`
3. Python 3.8+ for development
4. AWS SES


## AWS Setup
You need to load the email templates into AWS SES. The pre-built email templates are located at https://github.com/dataswift/email-templates/tree/master/data-passport/build

Then setup your AWS ENV variables so that you can call the SES.
Either put them in your `.aws/credentials` or the `.env` below.


## Development

### 1. Create and update local .env

``` Bash
cp .env.example .env
```

### 2. Run local api

``` Bash
docker-compose up
```
Tables will automatically be created.

### 3. Create the initial root user. This only needs to be done once.

Enter the db docker container
``` Bash
# Refer to your .env for <postgres_user> and <db_name>
docker-compose exec db psql -h localhost -U <postgres_user> <db_name>
```

You will be in the `psql` console
``` sql
# Make sure to update the email address and password below
INSERT INTO users(id, email, hashed_password, is_active, is_superuser, is_verified) VALUES (uuid_generate_v4(), '<root@localhost.local>', crypt('<password>', gen_salt('bf', 10)), true, true, true); 
```

`Ctrl-D` to exit

### 4. Upload Sample Data
#### Merchants Data
* Update the file `./test/data/merchant.csv` and add in your desired records.
* Open `http://localhost:<port>/api/docs`
* Log in to `Authorize` with the root user above.
* Go to the endpoint `GET /api/crm/merchants/upload` and upload your edited `merchant.csv` file

#### Customers Data
* Create a new csv file with the following header
`person.profile.first_name,person.profile.last_name,person.address.address_line_1,person.address.city,person.contact.email`
* Go to the endpoint `GET /api/crm/customers/upload` and upload your edited file

#### Looking at Customer Data
* Enter the db docker container (see upwards)
``` sql
SELECT * FROM customers limit 5;
```
The `id` is the `barcode`.
