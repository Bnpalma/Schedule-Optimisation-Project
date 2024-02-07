# setup.py
import pandas as pd
from pulp import LpProblem, LpMinimize

lp_problem = LpProblem("StaffSchedulingOptimization", LpMinimize)

# File path for the Excel file
excel_file_path = "/Users/bernardonobrepalma/Desktop/Projeto FIO CUF/DataCUF.xlsx"

# Read data from Excel file into DataFrames
staff_df = pd.read_excel(excel_file_path)
costs_df = pd.read_excel(excel_file_path,2)
overtime_cost_df = pd.read_excel(excel_file_path,3)
min_max_consec_work_hours_df = pd.read_excel(excel_file_path,7)
min_max_week_work_hours_df = pd.read_excel(excel_file_path, 9)
max_overtime_df = pd.read_excel(excel_file_path, 6)
min_staff_allocation_df = pd.read_excel(excel_file_path, 4)
max_staff_allocation_df = pd.read_excel(excel_file_path, 5)
minRestHoursbetweenShifts_df =  pd.read_excel(excel_file_path, 8)


# Extract data from DataFrames
RoleID = staff_df.iloc[3:38, 1].dropna().tolist() 
DeptID = staff_df.iloc[3:11, 5].dropna().tolist()  
Time = staff_df.iloc[4:28, 7].dropna().tolist()
Days = staff_df.iloc[4:11, 10].dropna().tolist()
StaffID = staff_df.iloc[4:743, 16].dropna().tolist()
Shift = staff_df.iloc[3:6, 13].dropna().tolist()
allowedStartHours = staff_df.iloc[14:20, 4].dropna().tolist()
allowedEndHours = staff_df.iloc[22:28, 4].dropna().tolist()

costPerHour = costs_df.iloc[3:41, 1].dropna().tolist()
overtimeCost = overtime_cost_df.iloc[3:41, 1].dropna().tolist()
StaffAvailableperRole = staff_df.iloc[3:41, 2].dropna().tolist()

maxRegularHours = staff_df.iloc[29, 4] 
maxConsecutiveWorkHours = min_max_consec_work_hours_df.iloc[4:41, 6].dropna().tolist()
minConsecutiveWorkHours = min_max_consec_work_hours_df.iloc[4:41, 1].dropna().tolist()
minRestHoursbetweenShifts = minRestHoursbetweenShifts_df.iloc[4:41:, 1]  
minHoursPerWeek = min_max_week_work_hours_df.iloc[4:41, 1].dropna().tolist()
maxHoursPerWeek = min_max_week_work_hours_df.iloc[4:41, 6].dropna().tolist()
maxOvertimePerWeek = max_overtime_df.iloc[4:41, 1].dropna().tolist()



min_staff_allocation_dict = {}
max_staff_allocation_dict = {}

# Start rows for each role's table (36 roles, each table with 10 rows, starting from row 4)
start_rows = [4 + i * 10 for i in range(36)] 
rows_per_table = 8  # Only 8 rows with information per role

for start_row, role_id in zip(start_rows, RoleID):
    # Selecting the range for each role's table
    allocation_matrix = max_staff_allocation_df.iloc[start_row:start_row + rows_per_table, 1:]
    allocation_matrix2 = max_staff_allocation_df.iloc[start_row:start_row + rows_per_table, 1:]
    
    # Filling NaN values with 0 and converting DataFrame to numpy array
    allocation_matrix = allocation_matrix.fillna(0).to_numpy()
    allocation_matrix2 = allocation_matrix2.fillna(0).to_numpy()
    min_staff_allocation_dict[role_id] = allocation_matrix
    max_staff_allocation_dict[role_id] = allocation_matrix2
