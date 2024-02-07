from setup import (
    lp_problem,
    StaffAvailableperRole,
    min_staff_allocation_dict,
    max_staff_allocation_dict,
    maxConsecutiveWorkHours,
    minConsecutiveWorkHours,
    minRestHoursbetweenShifts,
    maxRegularHours,
    maxOvertimePerWeek,
    minHoursPerWeek,
    maxHoursPerWeek,
    allowedStartHours,
    allowedEndHours,
    StaffID,
    RoleID,
    DeptID,
    Time,
    Days,
    Shift
)
from variables import timeIN, timeOUT, timeINot, timeOUTot, Allocation, withinShift, isOverMidnight


def add_constraints():
    # Constraint 1: Link Allocation with timeIN, timeOUT, timeINot, and timeOUTot
    for s in StaffID:
        for r in RoleID:
            for j in DeptID:
                for t in Time:
                    for d in Days:
                        lp_problem += Allocation[s][r][j][t][d] == sum(withinShift[s][r][j][d][sh] for sh in Shift)
                        
                        for sh in Shift:
                            lp_problem += withinShift[s][r][j][d][sh] == ((timeIN[s][r][j][d][sh] <= t) & (t <= timeOUT[s][r][j][d][sh])) | ((timeINot[s][r][j][d][sh] <= t) & (t <= timeOUTot[s][r][j][d][sh]))

    # Constraint 2: Ensure minimum staff allocation
    for j in DeptID:
        for r in RoleID:
            for t in Time:
                for d in Days:
                    lp_problem += sum(Allocation[s][r][j][t][d] for s in StaffID) >= min_staff_allocation_dict[r][j][t]

    # Constraint 3: Ensure staff available per role is not exceeded
    for r in RoleID:
        for t in Time:
            for d in Days:
                lp_problem += sum(Allocation[s][r][j][t][d] for j in DeptID for s in StaffID) <= StaffAvailableperRole[r]

    # Constraint 4: Ensure maximum and minimum consecutive work hours
    for stf in StaffID:
        for r in RoleID:
            for dep in DeptID:
                for d in Days:
                    for sh in Shift:
                        workHours = (timeOUT[stf][r][dep][d][sh] - timeIN[stf][r][dep][d][sh]) * (1 - isOverMidnight[stf][r][dep][d][sh]) + (timeOUT[stf][r][dep][(d + 1) % len(Days)][sh] + 24 - timeIN[stf][r][dep][d][sh]) * isOverMidnight[stf][r][dep][d][sh]
                        lp_problem += workHours >= minConsecutiveWorkHours
                        lp_problem += workHours <= maxConsecutiveWorkHours

   # Constraint 5: Min rest hours between "shifts" (including overtime)
    for stf in StaffID:
        for r in RoleID:
            for dep in DeptID:
                for d in Days:
                    for sh in Shift:
                        nextShift = (sh + 1) % len(Shift)
                        nextDay = (d + 1) % len(Days)
                        
                        # Regular case (within the same day)
                        lp_problem += (timeIN[stf][r][dep][d][nextShift] - timeOUT[stf][r][dep][d][sh] >= minRestHoursbetweenShifts)
                        lp_problem += (timeINot[stf][r][dep][d][nextShift] - timeOUTot[stf][r][dep][d][sh] >= minRestHoursbetweenShifts)

                        # Spanning two days
                        lp_problem += (timeIN[stf][r][dep][nextDay][nextShift] - timeOUT[stf][r][dep][d][sh] + 24 >= minRestHoursbetweenShifts)
                        lp_problem += (timeINot[stf][r][dep][nextDay][nextShift] - timeOUTot[stf][r][dep][d][sh] + 24 >= minRestHoursbetweenShifts)

    # Constraint 6: Staff start and finish working at specific hours
    for stf in StaffID:
        for r in RoleID:
            for dep in DeptID:
                for d in Days:
                    for sh in Shift:
                        # Start time constraints for regular shifts
                        lp_problem += sum(timeIN[stf][r][dep][d][sh] == i for i in allowedStartHours) == 1
                        
                        # End time constraints for regular and overtime shifts
                        lp_problem += sum(timeOUT[stf][r][dep][d][sh] == j for j in allowedEndHours) == 1

    # Constraint 7: Overtime hours calculation
    for stf in StaffID:
        for r in RoleID:
            for dep in DeptID:
                for d in Days:
                    for sh in Shift:
                        # Start of overtime
                        lp_problem += timeINot[stf][r][dep][d][sh] >= timeIN[stf][r][dep][d][sh] + maxRegularHours

                        # Limit of overtime hours
                        overtimeHours = (timeOUTot[stf][r][dep][d][sh] - timeINot[stf][r][dep][d][sh]) * (1 - isOverMidnight[stf][r][dep][d][sh]) + (timeOUTot[stf][r][dep][(d + 1) % len(Days)][sh] + 24 - timeINot[stf][r][dep][d][sh]) * isOverMidnight[stf][r][dep][d][sh]
                        lp_problem += overtimeHours <= maxConsecutiveWorkHours - maxRegularHours

    # Constraint 8: Ensure maximum overtime hours per week and maximum and minimum regular hours per week
    for stf in StaffID:
        for r in RoleID:
            for dep in DeptID:
                # Sum of regular hours per week
                regularHoursPerWeek = sum((timeOUT[stf][r][dep][d][sh] - timeIN[stf][r][dep][d][sh]) * (1 - isOverMidnight[stf][r][dep][d][sh]) + (timeOUT[stf][r][dep][(d + 1) % len(Days)][sh] + 24 - timeIN[stf][r][dep][d][sh]) * isOverMidnight[stf][r][dep][d][sh] for d in Days for sh in Shift)
                lp_problem += regularHoursPerWeek <= maxHoursPerWeek[r]
                lp_problem += regularHoursPerWeek >= minHoursPerWeek[r]

                # Sum of overtime hours per week
                overtimeHoursPerWeek = sum((timeOUTot[stf][r][dep][d][sh] - timeINot[stf][r][dep][d][sh]) * (1 - isOverMidnight[stf][r][dep][d][sh]) + (timeOUTot[stf][r][dep][(d + 1) % len(Days)][sh] + 24 - timeINot[stf][r][dep][d][sh]) * isOverMidnight[stf][r][dep][d][sh] for d in Days for sh in Shift)
                lp_problem += overtimeHoursPerWeek <= maxOvertimePerWeek


# Call the function to add constraints
add_constraints()
