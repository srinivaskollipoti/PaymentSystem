use db;


INSERT INTO PAYMENT_METHOD (PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("CREDIT","8e28af1b-a3a0-43a9-96cc-57d66dd68294");
INSERT INTO PAYMENT_METHOD (PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("DEBIT","8e28af1b-a3a0-43a9-96cc-57d66dd68295");
INSERT INTO PAYMENT_METHOD (PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("CHECKINGS","8e28af1b-a3a0-43a9-96cc-57d66dd68296");
INSERT INTO PAYMENT_METHOD (PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("SAVINGS","8e28af1b-a3a0-43a9-96cc-57d66dd68297");

INSERT INTO USER values ("e588ab04-68df-11ed-b759-0242c0a89002","SRINIVAS","KOLLIPOTI","srinivaskollipoti@gmail.com");
INSERT INTO USER values ("e588ab04-68df-11ed-b759-0242c0a89993","SRINIVAS","KOLLIPO","srinukollipoti@gmail.com");
INSERT INTO USER values ("e588ab04-68df-11ed-b759-0242c0a89004","SRINIVAS","KL","srinivas@gmail.com");
INSERT INTO USER values ("e588ab04-68df-11ed-b759-0242c0a89995","SRINIVAS","SHARMA","srk@gmail.com");

INSERT INTO USER_PAYMENT_METHOD (USER_ID,PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("e588ab04-68df-11ed-b759-0242c0a89002","CREDIT","8e28af1b-a3a0-43a9-96cc-57d66dd68294");
INSERT INTO USER_PAYMENT_METHOD (USER_ID,PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("e588ab04-68df-11ed-b759-0242c0a89002","CREDIT","8e28af1b-a3a0-43a9-96cc-57d66dd68296");
INSERT INTO USER_PAYMENT_METHOD (USER_ID,PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("e588ab04-68df-11ed-b759-0242c0a89002","SAVINGS","8e28af1b-a3a0-43a9-96cc-57d66dd68297");
INSERT INTO USER_PAYMENT_METHOD (USER_ID,PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("e588ab04-68df-11ed-b759-0242c0a89993","CREDIT","8e28af1b-a3a0-43a9-96cc-57d66dd68295");
INSERT INTO USER_PAYMENT_METHOD (USER_ID,PAYMENT_TYPE,PAYMENT_TYPE_ID) VALUES ("e588ab04-68df-11ed-b759-0242c0a89995","CREDIT","8e28af1b-a3a0-43a9-96cc-57d66dd68298");


INSERT INTO PAYMENT VALUES ("e8af92bd-1910-421e-8de0-cb3dcf9bf44d",
                            "4c3e304e-ce79-4f53-bb26-4e198e6c780a",
                            "8e28af1b-a3a0-43a9-96cc-57d66dd68294",
                            "USD",
                            70.0,
                            1,
                            "SUCCESS");