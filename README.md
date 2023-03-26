# swallet
## swallet is am E-Wallet backend api that allows user to create a wallet and deposit funds via mpesa express and c2b

## Getting started
1. cd into project and create a virtual environment and activate it
```
virtualenv -p python3.11 .venv
source .venv/bin/activate
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Run Migrations and create superuser
```
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
```
4. Create .env file inside swalletproject and copy the below code
```
SECRET_KEY=super_secret_key
HOST_DOMAIN=your_https_tunnel_or_domain_host(e.g pagekite)

SHORTCODE=174379
TESTMSISDN=254708374149
CONSUMER_KEY=your_saf_consumer_key
CONSUMER_SECRET=your_saf_consumer_secret
PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919

MPESA_AUTH_URL=https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials
MPESA_REGISTER_CALLBACK_URL=https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl
PROCESS_STKPUSH_URL=https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest
C2B_SIMULATE_URL=https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate
```
5. run tests
```
python manage.py test
```

6. Start the project
```
python manage.py runserver
```
## Swagger Endpoint documentation(get list of all endpoints and data required here)
### Go to the url {{host: e.g 127.0.0.1:8000}}/api/schema/swagger-ui/#/

[endpoints documentation](127.0.0.1:8000/api/schema/swagger-ui/#/)

## short description of logc
1. User registers account on register endpoint and a wallet created automatically upon creation which is related to the user and account number as the phone number which defaults to a balance of 0

2. username and password is required in the access_token endpoint which returns access token and refresh token

3. Protected endpoints are authenticated by passing in the access token in the headers in format Bearer <access_token>

4. authenticated user can call the balance endpoint and the wallet account balance is returned

## Deposit

## using stk push
Logged in User can call the stkpush process endpoint which he will provide the number_to_pay_with which will open the sim stk for pin on the number provided which when succesful will credit the logged in user wallet

## using c2b
the simulate c2b safaricom api is currently not working at the time of writing this readme
### Solution
Login to daraja and use the sandbox simulate c2b providing billrefnumber as the user accoount number which will receive the deposit

## Extras
-use the registerurls endpoint and provide your confirmation and validationurl that will be used to receive responses by safaricom c2b upon completion of the transaction


## Balances
-call the balance endpoint after transaction process to receive the updated wallet balance

## Online Version
[endpoints documentation](https://swalletserian.pythonanywhere.com/)

