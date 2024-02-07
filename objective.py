from pulp import lpSum, value
from setup import lp_problem
from variables import timeIN, timeOUT, timeOUTot, timeINot, isOverMidnight
from setup import costPerHour, overtimeCost, RoleID, DeptID, Days, Shift, StaffID

def set_objective():
    # Objective function components
    regular_hours_cost = lpSum(
        costPerHour[r] * (
            lpSum(
                (timeOUT[stf][r][j][d][sh] - timeIN[stf][r][j][d][sh]) * (1 - isOverMidnight[stf][r][j][d][sh]) +
                (timeOUT[stf][r][j][(d + 1) % len(Days)][sh] + 24 - timeIN[stf][r][j][d][sh]) * isOverMidnight[stf][r][j][d][sh]
                for stf in StaffID for sh in Shift
            )
        ) for r in RoleID for j in DeptID for d in Days
    )

    overtime_hours_cost = lpSum(
        overtimeCost[r] * (
            lpSum(
                (timeOUTot[stf][r][j][d][sh] - timeINot[stf][r][j][d][sh]) * (1 - isOverMidnight[stf][r][j][d][sh]) +
                (timeOUTot[stf][r][j][(d + 1) % len(Days)][sh] + 24 - timeINot[stf][r][j][d][sh]) * isOverMidnight[stf][r][j][d][sh]
                for stf in StaffID for sh in Shift
            )
        ) for r in RoleID for j in DeptID for d in Days
    )

    # Total Cost
    total_cost = regular_hours_cost + overtime_hours_cost

    # Set the objective
    lp_problem += total_cost

set_objective()
