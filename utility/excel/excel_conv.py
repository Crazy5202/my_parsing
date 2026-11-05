# import openpyxl
# from openpyxl import Workbook
# from openpyxl.styles import Alignment

# src = openpyxl.load_workbook("K5_init_merged.xlsx")
# ws = src.active

# customer_results_dict = {}

# row = ws.min_column
# left_col = ws.min_column

# while row <= ws.max_row:

#     cell_value = ws.cell(row=row, column=left_col).value

#     if isinstance(cell_value, str) and "Question" in cell_value.strip():

#         question_letter = cell_value.strip()[-2]

#         row += 1
#         while row <= ws.max_row:
#             left_value = ws.cell(row=row, column=left_col).value
#             if isinstance(left_value, str) and "Question" in left_value.strip():
#                 break
#             right_value = ws.cell(row=row, column=left_col+1).value.strip()

#             customer_info_list = left_value.splitlines()
#             customer_id = customer_info_list[0]

#             if not customer_id in customer_results_dict:
#                 customer_results_dict[customer_id] = {}
#             if not question_letter in customer_results_dict[customer_id]:
#                 customer_results_dict[customer_id][question_letter] = []

#             customer_results_dict[customer_id][question_letter].append([customer_info_list[1:].append(right_value)])
#             row += 1

# print(customer_results_dict)

#########################################################################################################################

# import openpyxl
# from openpyxl import Workbook
# from openpyxl.styles import Alignment

# src = openpyxl.load_workbook("K5_init_merged.xlsx")
# ws = src.active

# question_results_dict = {}

# row = ws.min_column
# left_col = ws.min_column
# right_col = left_col+1

# while row <= ws.max_row:

#     right_value = ws.cell(row=row, column=right_col).value

#     if not right_value:
#         question = ws.cell(row=row, column=left_col).value.strip()
#         question_results_dict[question] = []
#         row += 1
#     else:
#         while row <= ws.max_row:
#             right_value = ws.cell(row=row, column=right_col).value
#             if not right_value:
#                 break
#             left_value = ws.cell(row=row, column=left_col).value
            
#             customer_info_list = left_value.splitlines()
#             customer_info_list.append(str(right_value).strip())

#             question_results_dict[question].append(customer_info_list)

#             row += 1

# print(question_results_dict)

# out = Workbook()
# ows = out.active
# ows.append(["customer", "date", "rate", "comment"])

# for 

# for r in a_rows:
#     cust, user, date = split_respondent(ws.cell(row=r, column=1).value)
#     rate   = ws.cell(row=r, column=2).value
#     ans_b  = b_by_customer.get(cust, "")
#     comment = (f"Survey by {user} on {date} - rate: {rate}\n\n"
#                f"{b_text}:\n{ans_b}").rstrip()
#     ows.append([cust, date, rate, comment])

# # Allow multi-line comments to render.
# for cell in ows["D"][1:]:
#     cell.alignment = Alignment(wrap_text=True, vertical="top")

# out.save("survey_output.xlsx")

#########################################################################################################################

import sys
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment

if len(sys.argv) < 2:
    print("Usage: python <script_name>.py <input.xlsx> [output.xlsx]")
    sys.exit(1)

SRC = sys.argv[1]
DST = sys.argv[2] if len(sys.argv) > 2 else "automerged_data.xlsx"

try:
    src = openpyxl.load_workbook(SRC)
    ws = src.active

    question_store_dict = {}
    qsd_counter = 0

    customer_results_dict = {}

    row = ws.min_row
    left_col = ws.min_column
    right_col = left_col+1

    while row <= ws.max_row:
        left_val = ws.cell(row=row, column=left_col).value
        right_val = ws.cell(row=row, column=right_col).value

        if left_val is None:
            row += 1
            continue

        left_val = str(left_val).strip()
        if not "\n" in left_val:
            current_question_num = qsd_counter
            if not left_val in question_store_dict:
                question_store_dict[left_val] = current_question_num
                qsd_counter += 1
            row += 1
            continue
        
        parts = left_val.splitlines()
        while len(parts) < 3:
            parts.append("")
        customer, user, date = parts

        answer = str(right_val).strip() if right_val is not None else ""

        customer_results_dict.setdefault(customer, {}) \
            .setdefault(date, {}) \
            [current_question_num] = [user, answer]

        row += 1

    #print(customer_results_dict)

    out = Workbook()
    ows = out.active
    ows.append(["customer", "date", "rate", "comment"])

    for customer, date_actions in customer_results_dict.items():
        for date, qanswers in date_actions.items():
            answer_a = qanswers[0]
            comment = f"Survey by {answer_a[0]} on {date} - rate: {answer_a[1]}"
            question_by_id = list(question_store_dict.keys())
            for question, answer in qanswers.items():
                if not question == 0:
                    comment += f'\n\n{question_by_id[question]}:\n{answer[1]}'
            ows.append([customer, date, answer_a[1], comment])

    for cell in ows["D"][1:]:
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    out.save(DST)
except Exception as e:
    print(f"Exception occurred: {e}")