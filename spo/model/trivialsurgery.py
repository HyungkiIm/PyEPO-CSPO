#!/usr/bin/env python
# coding: utf-8

import gurobipy as gp
from gurobipy import GRB
from spo.model import optModel

class trivialSurgeryModel(optModel):
    """optimization model for shortest path problem"""

    def __init__(self, K, num_surgeries):
        """
        Args:
            grid: size of grid network
        """
        self.k = K
        self.num_surgeries = num_surgeries
        super().__init__()

    @property
    def num_cost(self):
        return self.num_surgeries

    def _getModel(self):
        """
        Gurobi model
        """
        # ceate a model
        m = gp.Model('trivial surgery')
        # turn off output
        m.Params.outputFlag = 0
        # varibles
        self.x = m.addVars(self.num_surgeries, name='x', vtype=gp.GRB.BINARY)
        # sense
        m.modelSense = GRB.MINIMIZE
        # constraints
        m.addConstr(gp.quicksum(self.x) >= self.k)

        return m

    def setObj(self, c):
        """
        set objective function
        """
        assert len(c) == len(self.x), 'Size of cost vector cannot match arcs'
        obj = gp.quicksum(c[i] * self.x[i] for i in range(self.num_surgeries))
        self._model.setObjective(obj)

    def solve(self):
        """
        solve model
        """
        self._model.update()
        self._model.optimize()
        return [self.x[e].x for e in range(self.num_surgeries)], self._model.objVal

    def addConstr(self, coefs, rhs):
        """
        add new constraint
        """
        # assert len(coefs) == len(self.arcs), 'Size of coef vector cannot match arcs'
        # copy
        new_model = trivialSurgeryModel(self.k, self.num_surgeries)
        # add constraint
        new_model._model.addConstr(gp.quicksum(coefs[i] * new_model.x[i]
                                               for i in range(self.num_surgeries))
                                   == rhs)
        return new_model