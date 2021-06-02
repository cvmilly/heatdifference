#!/usr/bin/env python
# VM


import os
import sys

import numpy as np
import matplotlib.pyplot as plt



class DimHeatDist(object) :

    def __init__ (self, temperature, max_iter) :

        self.rows = temperature + 2
        self.cols = temperature + 2
        self.temperature = temperature

        ## halo cells not on left-wall are zeroes
        self.arr_cur = np.zeros((self.rows, self.cols), dtype = 'float')

        ## halo cell in left-wall are at constant temperature
        self.arr_cur[:, 0] = temperature

        self.colorlst = [ 'darkblue', 'blue', 'aqua', 'lawngreen', 'yellow','orange', 'red', 'darkred' ]
        self.arr_colors = np.linspace(0, temperature, len(self.colorlst) + 1)

        ## to track previous state
        self.arr_prev = self.arr_cur.copy()


    ##
    ## calc_temperature: at every cell, the current temperature is calculated
    ##     using the temperature at the cardinal neighbors at the previous state,
    ##     using following equation:
    ##           1
    ## temp[i,j]=-(oldTemp[i-1,j] + oldTemp[i+1,j] + oldTemp[i,j-1] + oldTemp[i,j+1])
    ##           4
    ##
    ##     calculation ends at convergence, where two consecutive iterations result in the same values
    ##     halo cells values are not changed
    ##
    def calc_temperature(self, max_iter) :
        cnt = 0
        state_convergence = False;

        ## stop when current state == previous state or MaxIter is reached
        while cnt < max_iter and state_convergence == False :
            for i in range(1, self.rows-1, 1) :
                for j in range(1, self.cols-1, 1) :
                    self.arr_prev[i,j] = self.arr_cur[i,j]
                    self.arr_cur[i,j] = 0.25 * (self.arr_prev[i-1,j] + self.arr_prev[i+1,j] + self.arr_prev[i,j-1] + self.arr_prev[i,j+1])
            cnt += 1
            # at the end of iteration, check if the current state is EXACTLY the same as the new state
            state_convergence = np.array_equal(self.arr_prev, self.arr_cur)

        return cnt


    def print_state(self, arr) :
        rows = len(arr)
        cols = len(arr[0])
        for i in range(rows-1, -1, -1) :
            print("[", end = " ")
            for j in range(0, cols, 1) :
                print("[{0},{1}]={2:.4f} ".format(i, j, arr[i, j]), end = " ")
            print("]\n")


    def print_curr_state(self) :
        print("Current State: ")
        self.print_state(self.arr_cur)


    def print_prev_state(self) :
        print("Previous State: ")
        self.print_state(self.arr_prev)



    # calculate color point based on temperature
    
    def get_temp_color(self, temperature, value) :
        cols = len(self.colorlst)
        for k in range(0, cols) :
            if value == temperature :
                cl = self.colorlst[cols-1]
                break
            elif value >= self.arr_colors[k] and value < self.arr_colors[k+1] :
                cl = self.colorlst[k]
                break
        return cl

    
    def show_plot(self) :
        plt.title("Starting Temperature: " + str(self.temperature))
        rows = len(self.arr_cur) - 1
        cols = len(self.arr_cur[0]) - 1
        plt.xlim(0, self.temperature + 1)
        plt.ylim(0, self.temperature + 1)
        plt.tick_params(bottom = True, top = True, left = True, right = True, direction = 'in')
        for j in range(1, rows) :
            for k in range(1, cols) :
                value = self.arr_cur[j,k]
                cl = self.get_temp_color(self.temperature, value)
                plt.scatter(k, j, c = cl, marker = "o", edgecolors = "black", linewidths = 0.25, s = 12.0)

        # Show the result in the plot window
        plt.show()


###############################################################################


def main() :
    
    maxIter = 3000
    temperature = int(input("Enter temperature: "))

    dhdObj = DimHeatDist(temperature, maxIter)

    cnt = dhdObj.calc_temperature(maxIter)
    dhdObj.show_plot()
    print("Total Iterations = {0}".format(cnt))

    return 1


#####################################################################

if __name__ == "__main__":
    main()
