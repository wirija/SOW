from abc import ABC, abstractmethod

class Income(ABC):
    def __init__(
        self,
        source_name: str,
        amount: float,
        frequency: str = "monthly",
        source:str = '',
    ):
        self.source_name = source_name
        self.amount = amount
        self.frequency = frequency
        self.source = source

    @abstractmethod
    def calculate_annual_income(self) -> float:
        pass


class EmploymentIncome(Income):
    def __init__(
        self,
        source_name: str,
        amount: float,
        frequency: str = "monthly",
        employer: str = "",
    ):
        super().__init__(source_name, amount, frequency)
        self.employer = employer

    def calculate_annual_income(self) -> float:
        return self.amount * 12 if self.frequency == "monthly" else self.amount


class BusinessIncome(Income):
    def __init__(
        self,
        source_name: str,
        amount: float,
        frequency: str = "monthly",
        business_name: str = "",
    ):
        super().__init__(source_name, amount, frequency)
        self.business_name = business_name

    def calculate_annual_income(self) -> float:
        return self.amount * 12 if self.frequency == "monthly" else self.amount


class InvestmentIncome(Income):
    def __init__(
        self,
        source_name: str,
        amount: float,
        frequency: str = "monthly",
        investment_type: str = "",
    ):
        super().__init__(source_name, amount, frequency)
        self.investment_type = investment_type

    def calculate_annual_income(self) -> float:
        return self.amount * 12 if self.frequency == "monthly" else self.amount


class InheritanceIncome(Income):
    def __init__(self, source_name: str, amount: float, received_year: int):
        super().__init__(source_name, amount, frequency="one-time")
        self.received_year = received_year

    def calculate_annual_income(self) -> float:
        return self.amount  # One-time income


class OtherIncome(Income):
    def __init__(
        self,
        source_name: str,
        amount: float,
        frequency: str = "monthly",
        description: str = "",
    ):
        super().__init__(source_name, amount, frequency)
        self.description = description

    def calculate_annual_income(self) -> float:
        return self.amount * 12 if self.frequency == "monthly" else self.amount
