# Store service project

Django project internet store

## Features
 - Confirmation email upon user registration
 - the ability to log in via github/gmail.
 - the possibility to pay for the purchase through the stripe service.
 - custom mixin for the title of each page.
 - custom context processor
 - Powerful admin page



## Installation
Python3 must be already installed

- Install local PostgresSQL or use [ElephantSQL](https://www.elephantsql.com/)
- create DB.


```shell
git clone ####
cd store-service/
python -m venv venv
venv\Scripts\activate (on Windows)
venv\bin\activate (on Linux)
pip install -r requirements.txt
```

Create an .env file:
````
POSTGRES_HOST=<your DB host>
POSTGRES_DB=<your DB name>
POSTGRES_USER=<your DB username>
POSTGRES_PASSWORD=<your DB user password>

to work with email confirmation:(u can create separate gmail adress)

EMAIL_HOST_USER=<your email address>  
EMAIL_HOST_PASSWORD=<you email password> 

to work with stripe:

STRIPE_PUBLIC_KEY=<your stripe public key>
STRIPE_SECRET_KEY=<your stripe secret key>
STRIPE_WEBHOOK_SECRET=<your stripe webhook secret>

````






### How to work with oauth
 - [github](https://learndjango.com/tutorials/django-allauth-tutorial) 
start watching with Github OAuth
 - [google](https://www.section.io/engineering-education/django-google-oauth/) 
start watching with Step 4 – Create and configure a new Google APIs project


### How to work with STRIPE!
 - register your account in [Stripe](https://stripe.com/)
 - need to head into our Stripe dashboard and grab our API keys.Take that key and store it in your .env
 - The Stripe CLI is very handy for testing webhooks. Simply install the [CLI](https://stripe.com/docs/stripe-cli) and login to your Stripe account so that you are ready to continue.
 - Once your CLI is installed and ready, run the following command in a new terminal: 
 - stripe listen --forward-to 127.0.0.1:8000/webhook/
 - You should notice in the terminal that Stripe gives you a webhook secret key. Take that key and store it in your .env


Run migrations and run server:
````
python manage.py migrate
python manage.py runserver
````

Now u can add some categories and products and test it.

P.S.

Use card 4242 4242 4242 4242 to test pay for products

