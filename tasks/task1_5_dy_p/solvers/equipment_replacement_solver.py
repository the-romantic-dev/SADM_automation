class EquipmentReplacementSolver:
    def __init__(self, new_equip_price: int, yearly_income: list[int], residual_value: list[int]):
        self.residual_value = residual_value
        self.yearly_income = yearly_income
        self.new_equip_price = new_equip_price

    @property
    def new_equip_profits(self):
        s = self.residual_value
        p = self.new_equip_price
        r = self.yearly_income
        return [s[t] - p + r[0] for t in range(len(self.residual_value))]


solver = EquipmentReplacementSolver(
    9,
    [10, 9, 8, 7, 6, 5, 4],
    [8, 7, 6, 5, 4, 3, 2]
)
print(solver.new_equip_profits)