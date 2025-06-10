from dataclasses import dataclass

import phonenumbers
import deepparse
from src.Objects.Customers.Incomes import EmploymentIncome
from src.Objects.Customers.Incomes import BusinessIncome
from src.Objects.Customers.Incomes import InvestmentIncome
from src.Objects.Customers.Incomes import InheritanceIncome
from src.Objects.Customers.Incomes import OtherIncome

"""
    Class for customers
    Customer can be an individual or an non-individual
"""
class Customer:

    def __init__(self):
        self.GroupCustomerID = ''
        self.CustomerID = ''
        self.FirstName = ''
        self.LastName = ''
        self.DOB = ''
        self.Age = ''
        self.CountryOfResidence = ''
        self.RiskAssessment = ''
        self.isActive = True

        # Customer basic information
        self.Nationalities = list(Nationality)
        self.EmailAddresses = list(EmailAddress)
        self.ContactInformations = list(ContactInformation)
        self.Addresses = list(Address) 


        # CUstomer background
        self.Educations = list(Education)

        # Source of Wealth
        self.EmploymentIncomes = list(EmploymentIncome)
        self.BusinessIncomes = list(BusinessIncome)
        self.InvestmentIncomes = list(InvestmentIncome)
        self.InheritanceIncomes = list(InheritanceIncome)
        self.OtherIncomes = list(OtherIncome)

    def __str__(self):
        return (
            f"First Name: {self.FirstName}\n"
            f"Last Name: {self.LastName}\n"
            f"Date of Birth: {self.DOB}\n"
            f"Nationality: {self.Nationalities}\n"
            f"Country of Residence: {self.CountryOfResidence}\n"
            f"Age: {self.Age}\n"
            f"Education": {self.Educations}"
        )

    def get_riskAssessment(
        self
    ):
        # TODO - Call LLM to get risk assessments
        return 


@dataclass
class Education: 
    def __init__(self):
        self.Name = ''
        self.StartDate = ''
        self.EndDate = ''
        self.CourseName = ''
        self.Level = ''

        
    def __str__(self):
        return (
            f"Name: {self.Name}\n"
            f"Start Date: {self.StartDate}\n"
            f"End Date: {self.EndDate}\n"
            f"Course Name: {self.CourseName}\n"
            f"Level: {self.Level}"
        )

@dataclass
class ContactInformation:
    def __init__(self):
        self.Type = ''
        self.ContactNumber = ''
        self.Country = ''
        self.CountryCode = ''
        self.AreaCode = ''
        self.DateAdded = ''
        self.ContactNumber_normalised = ''
        self.isCallback = False
        self.isActive = True

    def __str__(self):
        return (
            f"Contact Information:\n"
            f"Type: {self.Type}\n"
            f"Contact Number: {self.ContactNumber}\n"
            f"Normalised Number: {self.ContactNumber_normalised}\n"
            f"Country: {self.Country} (Code: {self.CountryCode})\n"
            f"Area Code: {self.AreaCode}\n"
            f"Date Added: {self.DateAdded}\n"
            f"Callback: {'Yes' if self.isCallback else 'No'}\n"
            f"Current: {'Yes' if self.isCurrent else 'No'}"
        )
    
    def normalise_number (self):
        parsed = phonenumbers.parse(self.CountryCode + self.AreaCode + self.ContactNumber)
        self.ContactNumber_normalised = parsed.national_number


@dataclass
class EmailAddress:
    def __init__ (self):
        self.EmailAddress = ''
        self.isPrimary = False
        self.isActive = False

    def __str__(self):
        return (
            f"Email Information:\n"
            f"Email Address: {self.EmailAddress}\n"
            f"Primary: {'Yes' if self.isPrimary else 'No'}\n"
            f"Active: {'Yes' if self.isActive else 'No'}"
        )


@dataclass
class Address:
    def __init__ (self):
        self.Type = ''
        self.Address = ''
        self.Address_normalised = ''
        self.Country = ''
        self.PostalCode = ''
        self.DateAdded = ''
        self.isMailingAddress = False
        self.isActive = True

    def __str__(self):
        return (
            f"Address Information:\n"
            f"Type: {self.Type}\n"
            f"Address: {self.Address}\n"
            f"Normalised Address: {self.Address_normalised}\n"
            f"Country: {self.Country}\n"
            f"Postal Code: {self.PostalCode}\n"
            f"Date Added: {self.DateAdded}\n"
            f"Mailing Address: {'Yes' if self.isMailingAddress else 'No'}\n"
            f"Current: {'Yes' if self.isCurrent else 'No'}"
        )


@dataclass
class Nationality:
    def __init__ (self):
        self.Nationality = ''
        self.StartDate = ''
        self.isActive = True

    def __str__(self):
        return (
            f"Nationality Information:\n"
            f"Nationality: {self.Nationality}\n"
            f"Start Date: {self.StartDate}"
        )
