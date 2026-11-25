# def calculate_tax(monthly_salary, sst_deduct):
#     yearly_salary = round(float(monthly_salary) * 12, 2)

#     # Define tax slabs and rates
#     tax_slabs = [
#         # (500000, 0.01),   # 1% for the first 500,000
#         (200000, 0.10),   # 10% for the next 200,000
#         (300000, 0.20),   # 20% for the next 300,000
#         (1000000, 0.30),  # 30% for the next 1,000,000
#         (3000000, 0.36),  # 36% for the next 3,000,000
#     ]
#     high_rate = 0.39  # Above 5,000,000 at 39%

#     # Initial tax amounts
#     sst = 0.0
#     income_tax = 0.0

#     if yearly_salary <= 500000:

#         if sst_deduct == "sst_deduct_true":
#             # return {"sst": round((float(yearly_salary)*0.01)/12, 2), "income_tax": 0.0, "total_tax": 0.0}
        
#             data = [
#                 {"name": "SST",  "Total": round((float(yearly_salary)*0.01)/12, 2)},
#                 {"name": "Income Tax",  "Total": 0.0},
#                 {"name": "Total Tax",  "Total": round((float(yearly_salary)*0.01)/12, 2)},
#             ]

#             return data
#         if sst_deduct == "sst_deduct_false":
#             # return {"sst": (float(0.0)), "income_tax": 0.0, "total_tax": 0.0}    
#             data = [
#                 {"name": "SST",  "Total": 0.0},
#                 {"name": "Income Tax",  "Total": 0.0},
#                 {"name": "Total Tax",  "Total": 0.0},
#             ]  
#             return data
#     remaining_salary = yearly_salary

#     # First Rs. 500,000 taxed at 1%, store in ssf
#     if remaining_salary > 500000:
#         if sst_deduct == "sst_deduct_true":
#             sst = round(5000/12, 2)  # Fixed tax for first slab
#         if sst_deduct == "sst_deduct_false":
#             sst = 0.0  # Fixed tax for first slab in case of ssf
#         remaining_salary -= 500000

#     # Apply progressive tax on remaining salary
#     for slab_limit, rate in tax_slabs:
#         if remaining_salary <= 0:
#             break

#         taxable_amount = min(remaining_salary, slab_limit)
#         tax = taxable_amount * rate
#         income_tax += tax
#         remaining_salary -= taxable_amount

#     # If salary exceeds Rs. 5,000,000, apply 39% on the rest
#     if remaining_salary > 0:
#         income_tax += remaining_salary * high_rate

#     income_tax = round(float(income_tax)/12, 2)

#     total_tax = sst + income_tax

#     # return {
#     #     "sst": sst,
#     #     "income_tax": income_tax,
#     #     "total_tax": total_tax
#     # }


#     deduction_list = []

#     sst_data = {"name":"SST", "Total":sst}
#     # renumerable_data = {"name":"renumerable_tax", "total": round(float(income_tax)/12, 2)}
#     renumerable_data = {"name":"Income Tax", "Total": round(float(income_tax), 2)}
#     # total_data = {"name":"total_tax", "total": round(float(total_tax)/12, 2)}
#     total_data = {"name":"Total Tax", "Total": round(float(total_tax), 2)}

#     deduction_list.append(sst_data)
#     deduction_list.append(renumerable_data)
#     deduction_list.append(total_data)
#     # return {
#     #     "sst": sst,
#     #     "income_tax": income_tax,
#     #     "total_tax": total_tax
#     # }

#     return deduction_list


# def calculate_tax(monthly_salary, sst_deduct):
#     yearly_salary = round(float(monthly_salary) * 12, 2)

#     SST_THRESHOLD = 1000000  # new: was 500,000
#     SST_RATE = 0.01

#     # FY 2083/84 slabs — apply to the portion ABOVE the SST threshold
#     tax_slabs = [
#         (500000, 0.10),    # next 500,000 (10,00,001–15,00,000) at 10%
#         (1000000, 0.20),   # next 1,000,000 (15,00,001–25,00,000) at 20%
#         (1500000, 0.27),   # next 1,500,000 (25,00,001–40,00,000) at 27%
#     ]
#     high_rate = 0.29  # above 40,00,000 — was 39%

#     sst = 0.0
#     income_tax = 0.0

#     if yearly_salary <= SST_THRESHOLD:
#         if sst_deduct == "sst_deduct_true":
#             sst_amount = round((yearly_salary * SST_RATE) / 12, 2)
#             data = [
#                 {"name": "SST", "Total": sst_amount},
#                 {"name": "Income Tax", "Total": 0.0},
#                 {"name": "Total Tax", "Total": sst_amount},
#             ]
#             return data
#         if sst_deduct == "sst_deduct_false":
#             data = [
#                 {"name": "SST", "Total": 0.0},
#                 {"name": "Income Tax", "Total": 0.0},
#                 {"name": "Total Tax", "Total": 0.0},
#             ]
#             return data

#     remaining_salary = yearly_salary

#     # SST portion: 1% on the first Rs 10,00,000 (was a flat 5,000 on first 500,000)
#     if remaining_salary > SST_THRESHOLD:
#         if sst_deduct == "sst_deduct_true":
#             sst = round((SST_THRESHOLD * SST_RATE) / 12, 2)  # 1% of 10,00,000, monthly
#         if sst_deduct == "sst_deduct_false":
#             sst = 0.0
#         remaining_salary -= SST_THRESHOLD

#     for slab_limit, rate in tax_slabs:
#         if remaining_salary <= 0:
#             break
#         taxable_amount = min(remaining_salary, slab_limit)
#         income_tax += taxable_amount * rate
#         remaining_salary -= taxable_amount

#     if remaining_salary > 0:
#         income_tax += remaining_salary * high_rate

#     income_tax = round(float(income_tax) / 12, 2)
#     total_tax = sst + income_tax

#     deduction_list = [
#         {"name": "SST", "Total": sst},
#         {"name": "Income Tax", "Total": round(float(income_tax), 2)},
#         {"name": "Total Tax", "Total": round(float(total_tax), 2)},
#     ]
#     return deduction_list

def calculate_tax(monthly_salary, sst_deduct):
    yearly_salary = round(float(monthly_salary) * 12, 2)

    SST_THRESHOLD = 1_000_000
    SST_RATE = 0.01

    # (slab width, rate), applied to the portion ABOVE the SST threshold
    TAX_SLABS = [
        (500_000, 0.10),
        (1_000_000, 0.20),
        (1_500_000, 0.27),
    ]
    HIGH_RATE = 0.29  # above 40,00,000

    # ---------- SST ----------
    sst = 0.0
    if sst_deduct == "sst_deduct_true":
        sst = round((min(yearly_salary, SST_THRESHOLD) * SST_RATE) / 12, 2)

    # ---------- Income tax, bracket by bracket ----------
    remaining = max(yearly_salary - SST_THRESHOLD, 0)
    lower = SST_THRESHOLD
    brackets = []

    for width, rate in TAX_SLABS:
        if remaining <= 0:
            break
        taxable = min(remaining, width)
        brackets.append({
            "name": f"Tax Bracket ({rate:.0%})",
            "rate": rate,
            "from": lower,
            "to": lower + width,
            "taxable_amount": round(taxable, 2),               # yearly amount in this slab
            "Total": round((taxable * rate) / 12, 2),          # monthly tax for this slab
        })
        remaining -= taxable
        lower += width

    if remaining > 0:  # anything above 40,00,000
        brackets.append({
            "name": f"Tax Bracket ({HIGH_RATE:.0%})",
            "rate": HIGH_RATE,
            "from": lower,
            "to": None,
            "taxable_amount": round(remaining, 2),
            "Total": round((remaining * HIGH_RATE) / 12, 2),
        })

    total_tax = round(sst + sum(b["Total"] for b in brackets), 2)

    return [
        {"name": "SST", "Total": sst},
        *brackets,
        {"name": "Total Tax", "Total": total_tax},
    ]


def calculate_net_salary(total_amount, tax_deduction):
    for item in tax_deduction:
        if item["name"] == "Total Tax":
            total_tax = item["Total"]
            break

    net_amount = total_amount - Decimal(total_tax)
    # net_amount = 0.0

    return net_amount

from decimal import Decimal

def calculate_totals(employee_data):
    totals = {}
    
    # Iterate over each employee data
    for employee in employee_data:
        
        # Sum total salary
        totals["total_salary"] = totals.get("total_salary", Decimal(0.0)) + employee.get("total_gross_salary", {}).get("total_salary", Decimal(0.0))
        
        # Sum net amount
        totals["net_amount"] = totals.get("net_amount", Decimal(0.0)) + employee.get("net_amount", Decimal(0.0))
        
        # # Sum up fund deductions dynamically
        # for deduction in employee.get("fund_deductions", []):
        #     deduction_name = deduction["name"]
        #     totals[deduction_name] = totals.get(deduction_name, Decimal(0.0)) + deduction["amount"]
        
        # Sum up tax deductions dynamically
        for tax in employee.get("tax_deduction", []):
            # tax_name = tax["name"].lower()  # Normalize the tax name to lowercase for consistency
            tax_name = tax["name"]  # Normalize the tax name to lowercase for consistency
            totals[tax_name] = totals.get(tax_name, Decimal(0.0)) + Decimal(tax["Total"])
    
    return totals


import nepali_datetime
def get_nepali_date():

    # Get today's Nepali date
    today_nepali = nepali_datetime.date.today().strftime("%d %B %Y")
    # Get Nepali month and date
    nepali_month = nepali_datetime.date.today().strftime("%B")

    return nepali_month, today_nepali


def calculate_tax_yearly(yearly_salary, sst_deduct):
    yearly_salary = round(float(yearly_salary), 2)

    SST_THRESHOLD = 1000000
    SST_RATE = 0.01

    tax_slabs = [
        (500000, 0.10),
        (1000000, 0.20),
        (1500000, 0.27),
    ]
    high_rate = 0.29

    sst = 0.0
    income_tax = 0.0

    if yearly_salary <= SST_THRESHOLD:
        if sst_deduct == "sst_deduct_true":
            sst_amount = round(yearly_salary * SST_RATE, 2)
            return [
                {"name": "SST", "Total": sst_amount},
                {"name": "Income Tax", "Total": 0.0},
                {"name": "Total Tax", "Total": sst_amount},
            ]
        if sst_deduct == "sst_deduct_false":
            return [
                {"name": "SST", "Total": 0.0},
                {"name": "Income Tax", "Total": 0.0},
                {"name": "Total Tax", "Total": 0.0},
            ]

    remaining_salary = yearly_salary

    if remaining_salary > SST_THRESHOLD:
        if sst_deduct == "sst_deduct_true":
            sst = round(SST_THRESHOLD * SST_RATE, 2)  # 1% of 10,00,000 — yearly, no /12
        if sst_deduct == "sst_deduct_false":
            sst = 0.0
        remaining_salary -= SST_THRESHOLD

    for slab_limit, rate in tax_slabs:
        if remaining_salary <= 0:
            break
        taxable_amount = min(remaining_salary, slab_limit)
        income_tax += taxable_amount * rate
        remaining_salary -= taxable_amount

    if remaining_salary > 0:
        income_tax += remaining_salary * high_rate

    income_tax = round(float(income_tax), 2)  # no /12 — stays yearly
    total_tax = round(sst + income_tax, 2)

    return [
        {"name": "SST", "Total": sst},
        {"name": "Income Tax", "Total": income_tax},
        {"name": "Total Tax", "Total": total_tax},
    ]