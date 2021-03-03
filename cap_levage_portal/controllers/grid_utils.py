import logging

from odoo.addons.website_sale.controllers.main import TableCompute

_logger = logging.getLogger(__name__)


class TableComputeCapLevage(TableCompute):
    """"""

    def process(self, items, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in items:
            x = min(1, ppr)  # E-cosi Modif ici car on nos matéreils prennent tj 1 case
            y = min(1, ppr)  # E-cosi Modif ici car on nos matéreils prennent tj 1 case
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            # if index >= ppg and ((pos + 1.0) // ppr) > maxy:
            #     break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                "item": p,  # E-cosi Modif ici renomer 'product' en 'item'
                "x": x,
                "y": y,
                "class": "oe_ribbon_promo",  # E-cosi Modif ici car on a pas de classe custom
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows
