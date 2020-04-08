# Unloved functions

# From solar_power class:
    def find_optimal_dimensions_wrong(self):
        """
        Wrong. It selects the very small values at the beginning. You have to find the greatest 2nd derivative instead.
        """

        min_product_index = 0
        min_product = self.ans[0][0]*self.ans[0][1]

        for i in range(0,len(self.ans),1):
            if self.ans[i][0]*self.ans[i][1] < min_product or min_product == 0:
                min_product = self.ans[i][0]*self.ans[i][1]
                min_product_index = i

                print(i, ":", self.ans[min_product_index])

        return self.ans[min_product_index]
