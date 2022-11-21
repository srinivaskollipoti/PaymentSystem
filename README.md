# Intuit-Payment-System

# A Peer to Peer Distributed Payment System 


## Introduction

A peer to peer distributed payment system that can be integrated to one of the Intuit products.

Payment Service: A micro-service to publish new payments into a message queue, fetch payees and payment methods.

Rabbit MQ: A messaging queue which subscribe to Payment Service and publish to Risk Engine service.

Risk Service: Consume message from RabbitMQ queue and perform risk analysis on the transaction.

Mysql: A Relational database which holds users and payments data.

## [Directory Structure](#Directory Structure)
     payment_service : A Python based microservices
     risk_service    : A Python based microservices
     mysql           : A MySQL schema and test data


### System Design

<img width="682" alt="Screen Shot 2022-11-18 at 5 58 09 PM" src="https://user-images.githubusercontent.com/54916661/202824572-ad4ca32b-3636-4130-9d21-2443f95c2203.png">


## System Requirements:

1. Docker version 20.10.21
2. Python version > 3.8
3. Preferred IDE (VS CODE, PyCharm)
4. Postman

To install Docker, go to Docker official page (https://docs.docker.com/engine/install/), Download the executable based on your machine platform and run the executable on the machine.

To run the project on your machine, please follow the steps mentioned below:

## Setup:

     Step-1. Open terminal. 

     Step-2. Clone the repository by using the below command in the terminal

     ```git clone https://github.com/srinivaskollipoti/payements/edit/srini/payments.git``` 

     Step-3. Open the terminal and run the following command

     ```docker --version``` . This command should result in docker version verifying successful installation of docker.

     NOTE: In mac docker compose is installed with docker, but you may need to install it separately for other operating systems. Please refer: https://docs.docker.com/compose/install/

     Step-4. Run the following command from the project home directory ```docker-compose build``` (This might take a while to build the images locally.) 

     NOTE: There are variations to docker compose command. If ```docker-compose build``` does not work for you, try ```docker compose build```.

     Step-5. Verify successful docker image build using command ```docker images``` . (This command will list images)

     Step-6. Run ```docker-compose up -d``` to run the containers (i.e our micro-services).

     Step-7. Run ```docker ps``` to list the containers of the application. ( i.e payment_service, risk_service, rabbitmq, mysql).

     Step-8. Now the micro-services are up and running, launch Postman to Test Services. 

     Note: Please refer to port details in docker-compose.yml file and make sure used ports are available. 


## Design Decisions:

     Create Payment:
          1. Assuming paymentMethodId exist for the user. 
          2. A different service will be used to add new payment methods for a user.
     
     List All Supported Payments:
          1. Assuming we are talking about user's payment methods and a user can add multiple CREDIT, DEBIT, BANKING, CHECKING accounts. 
          2. A valid userId is provided as query param. Returns all user's supported payment methods.
          Note: /mysql/data.sql & /mysql/test-data.sql embodies the tabular structure for User Payment Methods.
     
     List All Payees:
          1. A user can search a payee with first name and last name. 
          2. There can be multiple customers with same first name and last name. Service will return a list. Email id in the respponse can be used to select the unique payee.

## Test Services:

1. Make a New Payment
Use the endpoint ```POST - http://localhost:5000/v1/payments``` to process new payment. 

A sample payload :

        {
                "amount":108888.0,
                "currency":"USD",
                "userId":"8e28af1b-a3a0-43a9-96cc-57d66dd68565",
                "payeeId":"8e28af1b-a3a0-43a9-96cc-57d66dd68267",
                "paymentMethodId":"8e28af1b-a3a0-43a9-96cc-57d66dd68294"
        }
        
2. List all the payment-methods a user constitutes
   Use the endpoint  ```GET - http://localhost:5000/v1/payment-methods?userId={}```.

3. List all the Payees 
   Use the endpoint ```GET - http://localhost:5000/v1/payees?firstName={}&lastName={}```. 
   

 MySQL database constitutes all the payment details and a snapshot of the PAYMENTS table :
 
 <img width="700" alt="Screen Shot 2022-11-18 at 7 41 02 PM" src="https://user-images.githubusercontent.com/54916661/202826442-30d10ec5-3315-4c66-b2e7-0b158c5c0ad0.png">
       
## Next Steps: 

1) Design Front-End component to initiate peer to peer payment through mobile/web based UI.
2) Add Authentication for the API's currently exposed.
3) Deploy multiple instances of RISK-ENGINE to attain horizontal scalability.
4) Host the docker images of application to AWS-ECR or equivalent cloud service and run multiple instances of micoservices through AWS-ECS or equivalent cloud services.
5) Use a Machine learning model to generate risk score for each transaction.


## Design & Development Standards:
- Coding styles, coding standards were followed throughout the project development. All the modules, classes and functions are inline documented.

- Test cases and development  
     1. The project is being built in stages, with the overall functionality being broken down into smaller modules and milestones. Throughout the project's development, a test-driven development approach is used.
     2. Multiple Testcases were added to validate different functions that were written during code development with usecases.
- Technical documentation is shared providing all the required information about each python module.   

## Test Suite:

   To run the test_suite of payment-service, navigate to payment-service folder and run : 

        python3 -m pytest tests/

   To run the test_suite of risk-engine, navigate to risk-engine folder and run:

        python3 -m pytest tests/




