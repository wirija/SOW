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
        self.FirstName = ''
        self.LastName = ''
        self.DOB = ''
        self.Nationality = ''
        self.CountryOfResidence = ''
        self.Age = ''
        self.RiskAssessment = ''
        self.Educations = list(Education)
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
            f"Nationality: {self.Nationality}\n"
            f"Country of Residence: {self.CountryOfResidence}\n"
            f"Age: {self.Age}"
            f"Education": {self.Educations}
        )

    def get_riskAssessment(
        self
    ):
        # TODO - Call LLM to get risk assessments

        
        return 


@property
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
