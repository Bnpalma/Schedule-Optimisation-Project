from pulp import LpVariable
from setup import lp_problem, RoleID, DeptID, Time, Days, StaffID, Shift

from pulp import LpVariable
from setup import lp_problem, StaffID, RoleID, DeptID, Days, Shift


# timeIN: When each staff member starts working
timeIN = LpVariable.dicts("timeIN", 
                          (StaffID, RoleID, DeptID, Days, Shift), 
                          lowBound=0, 
                          cat='Continuous')

# timeOUT: When each staff member finishes working
timeOUT = LpVariable.dicts("timeOUT", 
                           (StaffID, RoleID, DeptID, Days, Shift), 
                           lowBound=0, 
                           cat='Continuous')

# timeINot: Start of overtime
timeINot = LpVariable.dicts("timeINot", 
                            (StaffID, RoleID, DeptID, Days, Shift), 
                            lowBound=0, 
                            cat='Continuous')

# timeOUTot: End of overtime
timeOUTot = LpVariable.dicts("timeOUTot", 
                             (StaffID, RoleID, DeptID, Days, Shift), 
                             lowBound=0, 
                             cat='Continuous')

# withinShift: Boolean variable indicating if a staff member is within their shift
withinShift = LpVariable.dicts("withinShift", 
                               (StaffID, RoleID, DeptID, Days, Shift), 
                               cat='Binary')

# Allocation: Boolean variable for staff allocation
Allocation = LpVariable.dicts("Allocation", 
                              (StaffID, RoleID, DeptID, Time, Days), 
                              cat='Binary')

# isOverMidnight: Boolean variable indicating if the shift goes over midnight
isOverMidnight = LpVariable.dicts("isOverMidnight", 
                                  (StaffID, RoleID, DeptID, Days, Shift), 
                                  cat='Binary')