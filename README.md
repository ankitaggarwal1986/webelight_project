# webelight_project 

# code setup and installation
1. git clone https://github.com/ankitaggarwal1986/webelight_project.git
2. pip install -r requirements.txt
3. update the mysql database settings in .env file
4. python manage.py makemigrations   
5. python manage.py migrate
6. python manage.py runserver

# urls to follow
1. http://127.0.0.1:8000/api/register/     # to register the user
2. http://127.0.0.1:8000/api/login/        # to login the registerd user and make donation
3. enter the personal account of paypal sandbox given below to make payment.
4. the payment is accepted by paypal business account given below.



# Authentication
Used token based authentication as not able to find any free service to integrate otp authentication

# Payment gateway
paypal payment gateway is used in developers evvironment.

sandbox site : 'sandbox.paypal.com'
personal account : donatex@gmail.com            # this account is used for making payments"
personal account pass: Webelightsolutions@2

business email : "donatexbiz@gmail.com"         # this account is used for accepting payments"
password : Webelightsolutions@2

# Payment History

After logging in user has the option to view his transection history 