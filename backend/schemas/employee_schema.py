from pydantic import BaseModel
from typing import Literal


class employee_schema(BaseModel):
    Age: int
    BusinessTravel: Literal[
        "Non-Travel",
        "Travel_Rarely",
        "Travel_Frequently"
    ]

    Department: Literal[
        "Sales",
        "Research & Development",
        "Human Resources"
    ]
    Education: int

    EducationField: Literal[
        "Life Sciences",
        "Medical",
        "Marketing",
        "Technical Degree",
        "Human Resources",
        "Other"
    ]
   
    EnvironmentSatisfaction: int

    Gender: Literal["Male", "Female"]

    JobInvolvement: int
    JobLevel: int

    JobRole: Literal[
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Sales Representative",
        "Research Director",
        "Human Resources"
    ]

    JobSatisfaction: int

    MaritalStatus: Literal[
        "Single",
        "Married",
        "Divorced"
    ]

    MonthlyIncome: int

    OverTime: Literal["Yes", "No"]

    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsWithCurrManager: int