"""
Created on 30-Aug-2020
iBank Loan Approval System
@author: Kanwar Jot
"""

from abc import ABCMeta, abstractmethod
import json


with open("approved_loans.json", "r") as f:
    approved_loans_dict = json.load(f)


class InvalidLoanType(Exception):
    pass


class InsufficientSalary(Exception):
    pass


class Customer:
    try:
        __customer_id_last = int(max(approved_loans_dict.keys()))
    except ValueError:
        __customer_id_last = 0

    def __init__(self, loan_type, monthly_salary):
        self.__loan_type = loan_type
        self.__monthly_salary = monthly_salary
        self.__loan = None
        self.__customer_id = Customer.__customer_id_last + 1
        Customer.__customer_id_last += 1

    def apply_loan(self):
        if self.__loan_type in ("Home Loan", "Personal Loan"):
            if self.__loan_type == "Home Loan":
                loan = HomeLoan()
                if loan.calculate_amount_interest_rate(self.__monthly_salary) != -1:
                    self.__loan = loan
                else:
                    print("Insufficient Monthly Salary for Home Loan")
                    return -1
            else:
                loan = PersonalLoan()
                if loan.calculate_amount_interest_rate(self.__monthly_salary) != -1:
                    self.__loan = loan
                else:
                    print("Insufficient Monthly Salary for Personal Loan")
                    return -1
        else:
            raise InvalidLoanType

    def get_customer_id(self):
        return self.__customer_id

    def get_loan_type(self):
        return self.__loan_type

    def get_monthly_salary(self):
        return self.__monthly_salary

    def get_loan(self):
        return self.__loan


class Loan(metaclass=ABCMeta):
    __loan_counter = 1001

    def __init__(self):
        self.__loan_amount = None
        self.__interest_rate = None
        self.__loan_id = None

    def generate_loan_id(self):
        self.__loan_id = Loan.__loan_counter
        Loan.__loan_counter += 1

    @abstractmethod
    def calculate_amount_interest_rate(self, monthly_salary):
        pass

    def set_loan_amount(self, loan_amount):
        self.__loan_amount = loan_amount

    def set_interest_rate(self, interest_rate):
        self.__interest_rate = interest_rate

    def get_loan_id(self):
        return self.__loan_id

    def get_loan_amount(self):
        return self.__loan_amount

    def get_interest_rate(self):
        return self.__interest_rate


class HomeLoan(Loan):
    def __init__(self):
        self.__points = 5
        super().__init__()

    def get_points(self):
        return self.__points

    def calculate_amount_interest_rate(self, monthly_salary):
        if monthly_salary >= 20000:
            self.set_loan_amount(15 * monthly_salary)
            self.set_interest_rate(15)
            self.generate_loan_id()
        else:
            raise InsufficientSalary


class PersonalLoan(Loan):
    def __init__(self):
        self.__gift_voucher = 500

    def get_gift_voucher(self):
        return self.__gift_voucher

    def calculate_amount_interest_rate(self, monthly_salary):
        if monthly_salary >= 7000:
            self.set_loan_amount(7 * monthly_salary)
            self.set_interest_rate(12)
            self.generate_loan_id()
        else:
            raise InsufficientSalary


# instantiating customers
try:
    print("Welcome to iBank")
    loan_type_ = input("Please choose your Loan Type:\n\tHome Loan\n\tPersonal Loan\n")
    monthly_sal = eval(input("Please input your monthly salary(Rs.): "))
    customer_1 = Customer(loan_type_, monthly_sal)
    customer_1.apply_loan()
    print("Maximum Available Loan Details:\n\tCustomer ID: {}\n\tLoan Type: {}"
          "\n\tLoan Amount(Rs.): {}\n\tInterest Rate: {}\n\t".format(customer_1.get_customer_id(),
                                                                     customer_1.get_loan_type(),
                                                                     customer_1.get_loan().get_loan_amount(),
                                                                     customer_1.get_loan().get_interest_rate()))
    with open("approved_loans.json", "w") as f:
        to_add = [customer_1.get_loan_type(),
                  customer_1.get_loan().get_loan_amount(),
                  customer_1.get_loan().get_interest_rate()]
        approved_loans_dict[str(customer_1.get_customer_id())] = to_add
        json.dump(approved_loans_dict, f)

except InvalidLoanType:
    print("Invalid Loan Type")
except InsufficientSalary:
    print("Insufficient Salary")
except Exception as e:
    print("Error :" + str(e))
finally:
    print("Thank you for choosing iBank")
