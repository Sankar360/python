""" python mysql connect """

import mysql.connector
from tabulate import tabulate
con = mysql.connector.connect(host="localhost",user="root",password="root",database="micky")

res = con.cursor()

""" customer signup """

def signup():
    customer_id = int(input("enter the customerid"))
    firstname = input("enter the firstname")
    city = input("enter the city")
    state = input("enter the state")
    qry = "insert into mouse values (%s,%s,%s,%s)"
    val = (customer_id,firstname,city,state)
    res.execute(qry,val)
    con.commit()
    print("registered succesfully")
def get_customer():#get customer list
    qry = "select customer_id from mouse"
    res.execute(qry)
    result = res.fetchall()
    list_of_ids = []
    for i in result:
        list_of_ids.append(i[0])
    return list_of_ids
def get_order():
    customer_id = int(input("enter the customer_id"))
    qry = "select order_id from customer where customer_id = %s"
    val = (customer_id,)
    res.execute(qry,val)
    result = res.fetchall()
    list_of_order = []
    for i in result:
        list_of_order.append(i[0])
    return list_of_order

""" customer login """


def login():
    customer_id = int(input("enter the customer_id"))
    cust_list = get_customer()
    if customer_id in cust_list:
        
        user = int(input("enter the option\n1.view booking\n2.new booking\n3.cancel booking"))
        if user == 1:
            qry = "select * from orders where customer_id = %s"
            val = (customer_id,)
            res.execute(qry,val)
            result = res.fetchall()
            print(tabulate(result,headers=["orderid","customerid","productname","price","quantity","totalspend"]))
        elif user == 2:
            qry = "select productname,price from product"
            res.execute(qry)
            result = res.fetchall()
            print(tabulate(result,headers=["productname","price"]))
            productname = input("enter the product name")
            quantity = int(input("enter the quantity"))
            orderid = input("enter the orderid")
            qry = "select price from product where productname = %s"
            res.execute(qry,(productname,))
            price_res = res.fetchone()
            price_res = price_res[0]
            total_amount = quantity*price_res
            try:
                qry = "insert into customer values (%s,%s,%s,%s,%s)"
                val = (orderid,customer_id,productname,price_res,quantity)
                res.execute(qry,val)
                con.commit()
            except Exception as e:
                print("something went wrong")
            else:
                qry = "select quantity from product where productname = %s"
                val = (productname,)
                res.execute(qry,val)
                st_result = res.fetchone()
                stock = st_result[0]
                if stock<quantity:
                    print("out of stock")
                else:
                    cur_stock = stock - quantity
                    qry = "update product set quantity = %s where productname = %s"
                    val = (cur_stock,productname)
                    res.execute(qry,val)
                    con.commit()
        elif user == 3:
            order_id = int(input("enter the orderid:"))
            cust_ord_list = get_order()
            if order_id in cust_ord_list:
                qry = "select quantity  from customer where  order_id = %s"
                val = (order_id,)
                res.execute(qry,val)
                cn_qnt = res.fetchone()
                cn_qnt = cn_qnt[0]
                qry = "select productname  from  customer where  order_id = %s"
                val = (order_id,)
                res.execute(qry,val)
                cn_pro = res.fetchone()
                cn_pro = cn_pro[0]
                qry = "select quantity from product where productname = %s"
                val = (cn_pro,)
                res.execute(qry,val)
                st_result = res.fetchone()
                stock = st_result[0]
                updated_stk = stock+cn_qnt
                qry = "delete from customer where order_id = %s"
                val = (order_id,)
                res.execute(qry,val)
                con.commit()
                qry = "update product set quantity = %s where productname=%s"
                val = (updated_stk,cn_pro)
                res.execute(qry,val)
                con.commit()
                print("order cancelled")

""" employee signup """                
                
def emp_signup():
    emp_id=int(input("enter the emp_id:"))
    name=input("enter the name:")
    age=int(input("enter the age:"))
    email_id=input("enter the email_id:")
    qry="insert into employee values (%s,%s,%s,%s)"
    val=(emp_id,name,age,email_id)
    res.execute(qry,val)
    con.commit()
    print("emp_signup succesfully")
    
    
def get_employee():
    qry="select emp_id from employee"
    res.execute(qry,)
    result=res.fetchall()
    list_of_emp_ids=[]
    for i in result:
        list_of_emp_ids.append(i[0])
    return list_of_emp_ids 
        
""" employee login """


def emp_login():
    emp_id=int(input("enter the emp_id:"))
    emp_list=get_employee()
    if emp_id in emp_list:
        option=int(input("1.add product\n2.update quantity"))
        if option ==1:
            product_id=int(input("enter the product_id:"))
            productname = input("enter the product name")
            price=int(input("enter the price:"))
            quantity = int(input("enter the quantity"))
            qry="insert into product values(%s,%s,%s,%s)"
            val=(product_id,productname,price, quantity)
            res.execute(qry,val)
            con.commit()
            print("product added succesfully")
        elif option ==2:
            productname = input("enter the productname")
            size=int(input("enter the quantity of{productname}"))
            
            qry="select quantity from product where productname=%s"
            val=(productname,)
            res.execute(qry,val)
            st_result=res.fetchone()
            stock= st_result[0]
            total_uantity=int(stock)+size
            
            
            
            qry="update product set quantity=%s where productname=%s"
            val=(total_uantity,productname)
            res.execute(qry,val)
            con.commit()
            print("quantity updateed succesfully")

""" employee or customer select """

temp = input("A.customer or B.employee").upper()
if temp == "A":
    user = int(input("enter the option\n1.sign up\n2.login"))
    if user == 1:
        signup()
    elif user == 2:
        login()
elif temp == "B":
    user = int(input("enter the option\n1.sign up\n2.login"))
    if user == 1:
        emp_signup()
    elif user == 2:
        emp_login()

""" mysql """

""" create database micky;
use micky;
create table customer(
orderid int,
customerid int,
productname varchar(30),
price int,
quantity int
);
create table mouse(
customer_id int,
firstname varchar(20),
city varchar(25),
state varchar(30));
create table product(
product_id varchar(10),
productname varchar(20),
price int,
quantity int);

insert into product values
("1","laptop",10000,20),
("2","mobile",8000,45),
("3","projector",5000,25),
("4","mouse",100,200);


select * from customer;
select * from product;
select * from mouse;
set sql_safe_updates = 0;


create table employee(
emp_id int,
name varchar(50),
age int,
email_id varchar(100));
select * from employee
 """