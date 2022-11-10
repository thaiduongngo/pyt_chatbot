from datetime import date

full_name = "Modern Artificial Intelligence"
name = "MAI"
alias = name
# "2022-09-15"
dob = date(2022, 9, 15)
gender = "Female"
lang = "eng"
lang = lang.lower()
home_path = "/home/td/workspace/ml/pyt_chatbot/"
__author__ = "NtD"
__copyright__ = f"Copyright © 2022 {full_name} {__author__}"
__version__ = "0.1.0"


def age():
    today = date.today()
    delta_date = (today - dob).days
    if delta_date < 365:
        return f"{delta_date} days"
    else:
        delta_year = today.year - dob.year - (date(today.year, dob.month, dob.day) > today)
        return f"{delta_year} year(s)"


if __name__ == "__main__":
    print(name)
    print(dob)
    print(gender)
    print(age())
