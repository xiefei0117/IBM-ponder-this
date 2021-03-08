# -*- coding: utf-8 -*-
"""
Model for solving IBM - ponder this Feb. 2021
Fei Xie
"""

import pyomo.environ as pyo


model = pyo.AbstractModel()
opt = pyo.SolverFactory('cplex')

model.m = pyo.Param(within=pyo.NonNegativeIntegers) # nums of rows
model.n = pyo.Param(within=pyo.NonNegativeIntegers) # nums of cols
model.t_length = pyo.Param(within=pyo.NonNegativeIntegers) # nums of cols

model.M_dummy = pyo.RangeSet(0, model.m + 1)
model.N_dummy = pyo.RangeSet(0, model.n + 1)
model.M = pyo.RangeSet(1, model.m)
model.N = pyo.RangeSet(1, model.n)
model.T = pyo.RangeSet(0, model.t_length)
model.K = pyo.Set()


model.D = pyo.Param(model.M, model.N, model.K)

#decision variables
model.x = pyo.Var(model.M_dummy, model.N_dummy, model.T, domain = pyo.Binary)


#objective function
def obj_expression(model):
    return sum(sum(model.x[i,j,0] for i in model.M) for j in model.N)

model.OBJ = pyo.Objective(rule=obj_expression)

#constraint 1 - Dummy boundary at rows 0 and m + 1 and cols 0 and n + 1
def dummy_x_constraint_rule(model, i, j):
    if i == 0 or i == model.m + 1 or j == 0 or j == model.n + 1:
        return model.x[i,j,0] == 1
    else:
        return pyo.Constraint.Skip

model.dummy_x_constraint = pyo.Constraint(model.M_dummy, model.N_dummy, rule = dummy_x_constraint_rule)

#Dummy boundary at rows 0 and m + 1 and cols 0 and n + 1
#constraint 2-5
def vaccine_neccessary_condition_rule(model, i, j, t, k):
    if t < model.t_length:
        if k == "N":
            return model.D[i,j,k] * model.x[i,j,t+1] <= model.x[i-1, j, t] + model.x[i,j,t]
        elif k == "E":
            return model.D[i,j,k] * model.x[i,j,t+1] <= model.x[i, j+1, t] + model.x[i,j,t]
        elif k == "S":
            return model.D[i,j,k] * model.x[i,j,t+1] <= model.x[i+1, j, t] + model.x[i,j,t]
        else:
            return model.D[i,j,k] * model.x[i,j,t+1] <= model.x[i, j-1, t] + model.x[i,j,t]
    else:
        return pyo.Constraint.Skip

model.vaccine_neccessary_condition = pyo.Constraint(model.M, model.N, model.T, model.K, rule = vaccine_neccessary_condition_rule)

#constraint 6
def vaccine_sufficient_condition_rule(model, i, j, t):
    if t < model.t_length:
        return model.x[i,j,t+1] >= model.D[i,j,"N"]*model.x[i-1,j,t] + \
                                    model.D[i,j,"E"]*model.x[i,j+1,t] + \
                                    model.D[i,j,"S"]*model.x[i+1,j,t] + \
                                    model.D[i,j,"W"]*model.x[i,j-1,t] - \
                                    sum(model.D[i,j,k] for k in model.K) + 1
    else:
        return pyo.Constraint.Skip

#constraint 7 - final requirement for vaccination
def final_condition_rule(model, i, j, t):
    if t == model.t_length:
        return model.x[i,j,t] == 1
    else:
        return pyo.Constraint.Skip

model.final_condition = pyo.Constraint(model.M, model.N, model.T, rule = final_condition_rule)

#constraint 8 - Maintaining vaccine condition once vaccined
def maintain_vaccine_condition_rule(model, i, j, t):
    if t < model.t_length:
        return model.x[i,j,t+1] >= model.x[i,j,t]
    else:
        return pyo.Constraint.Skip

model.maintain_vaccine_condition = pyo.Constraint(model.M_dummy, model.N_dummy, model.T, rule = maintain_vaccine_condition_rule)

instance = model.create_instance("data_file.dat")
results = opt.solve(instance, tee=True)

outF = open("solutions.txt", "w")
for i in instance.M:
    for j in instance.N:
        outF.write(str(int(instance.x[i,j,0].value)))
    outF.write("\n")
    
outF.close()