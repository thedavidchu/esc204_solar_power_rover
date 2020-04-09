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

    #####

    def second_derivative(self,show=False):
        """
        Find the 'second derivative' of a discrete function by taking the second difference.

        Returns a list of second derivatives.

        X   X   X   X
          Y   Y   Y
            Z   Z
        
        """

        df = [None]
        d2f = [None]

        # Take first difference: f1 = (f(x+dx)-f(x))/dx
        for i in range(0,len(self.ans)-1,1):
            df += [int((self.ans[i+1][1] - self.ans[i][1]) / (self.ans[i+1][0] - self.ans[i][0]))]

        for i in range(1,len(self.ans)-1,1):
            d2f += [int((df[i+1] - df[i]) / (self.ans[i+1][0] - self.ans[i][0]))]
        d2f += [None]

        if show == True:
            print('First derivative:', df)
            print('Second derivative:', d2f)

        return d2f

    def find_max_d2f(self,show=False):
        d2f = self.second_derivative(show=show)
        max_d2f = 0
        max_index = 0
        
        for i in range(1,len(d2f)-1,1):
            if d2f[i] > max_d2f:
                max_d2f = d2f[i]
                max_index = i

        if show == True:
            print(d2f,'\n\n',d2f[0:1000])
            print('Largest Second Derivative:', max_index, self.ans[max_index], 'with d2f =', d2f[max_index])

        return max_index

    #####


    
