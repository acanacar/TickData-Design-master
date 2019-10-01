def calculatePV(A, n, r):
    total_PV = 0

    for i in range(n):
        k = 1 / (1 + r) ** i
        v = A * k
        total_PV += v
    return total_PV


def calculateDiscountRate(s, e, r):
    t = e - s
    return 1 / (1 + r) ** t


def calculateForwardRateForSpecificInterval(u, v, s_u, s_v):
    return ((1 + s_v) ** v / (1 + s_u) ** u) ** (1 / (v - u)) - 1


'''1.Question 1
Lottery payments

A major lottery advertises that it pays the winner $10 million. 
However this prize money is paid at the rate of $500,000 each year 
(with the first payment being immediate) for a total of 20 payments. 
What is the present value of this prize at 10% interest compounded annually?

Report your answer in $millions, rounded to two decimal places. So, for example, 
if you compute the answer to be 5.7124 million dollars then 
you should submit an answer of 5.71.'''

PV = calculatePV(A=500, n=20, r=0.1)
print("{:.2f}".format(PV))

'''2.Question 2
Sunk Costs (Exercise 2.6 in Luenberger)
A young couple has made a deposit of the first month's rent (equal to
$1,000) on a 6-month apartment lease. The deposit is refundable at
the end of six months if they stay until the end of the lease.
The next day they find a different apartment that they like just as well,
but its monthly rent is only $900. And they would again have to put a
deposit of $900 refundable at the end of 6 months.
They plan to be in the apartment only 6 months. 
Should they switch to the new apartment? Assume
an (admittedly unrealistic!) interest rate of 12% per month compounded monthly.'''

PV_q2 = {}
PV_q2['1'] = calculatePV(1000, 5, .01)
PV_q2['2'] = calculatePV(900, 5, .01) + 1000
if PV_q2['1'] >= PV_q2['2']:
    print('stay')
else:
    print('switch')

'''3.Question 3
Relation between spot and discount rates

Suppose the spot rates for 1 and 2 years are s_1 = 6.3\%s 
1=6.3% and s_2 = 6.9 with annual compounding. 
Recall that in this course interest rates are 
always quoted on an annual basis unless otherwise specified. 
What is the discount rate d(0,2)?
Please submit your answer rounded to three decimal places. 
So, for example, if your answer is 0:4567 then you should submit an answer of 0:457.'''

discount_rate_q3 = calculateDiscountRate(0, 2, 0.069)
print("{:.3f}".format(discount_rate_q3))

'''4.Question 4
Relation between spot and forward rates
Suppose the spot rates for 1 and 2 years are s_1 = 6.3\%s 
1=6.3% and s_2 = 6.9 with annual compounding. 
Recall that in this course interest rates are 
always quoted on an annual basis unless otherwise specified. 
What is the forward rate, f_{1_2} (forward rate 1-2) assuming annual compounding?

Please submit your answer as a percentage rounded to one decimal place so, for example, if your answer is 8.789% then you should submit an answer of 8.8.'''
fv_12_q4 = calculateForwardRateForSpecificInterval(1, 2, .063, .069)
print("{:.1f}".format(fv_12_q4 * 100))

'''5.Question 5
Forward contract on a stock

The current price of a stock is $400 per share and it pays no dividends. Assuming a constant interest rate of 
8% per year compounded quarterly, what is the stock's theoretical forward price for delivery in 9 months?
Please submit your answer rounded to two decimal places so for example, if your answer is 567.1234 then 
you should submit an answer of 567.12
'''
fv_price_q5 = 400 / calculateDiscountRate(0, 3, .02)
print('{:.2f}'.format(fv_price_q5))

"""
6.Question 6
Bounds using different lending and borrowing rate
Suppose the borrowing rate r_B = 10 compounded annually. However,
the lending rate (or equivalently, the interest rate on deposits) is
only 8% compounded annually. Compute the difference between the upper
and lower bounds on the price of an perpetuity that pays A=10,000$ per
year.

Please submit your answer rounded to the nearest dollar so if your answer is 23,456.78923,456.789 
then you should submit an answer of 2345723457."""


def calculateLoverUpperBoundOfPerpetuity(A, r_b, r_l):
    return round(A / r_l - A / r_b, 1)


difference_lower_upper_bounds_perpetuity = calculateLoverUpperBoundOfPerpetuity(10000, 0.1, .08)
print(difference_lower_upper_bounds_perpetuity)

"""# 7. Value of a Forward contract at an intermediate time
# Suppose we hold a forward contract on a stock with expiration 6 months from now. We entered into this contract 6
# months ago so that when we entered into the contract, the expiration was T=1 year. The stock price$ 6 months ago was
# S0=100, the current stock price is 125 and the current interest rate is r=10% compounded semi-annually. (This is the
# same rate that prevailed 6 months ago.) What is the current value of our forward contract?
# Please submit your answer in dollars rounded to one decimal place so if your answer is 42.678 then you should submit
# an answer of 42.7."""


def calculateCurrentValueOfForward(t=1, T=2, s_0=100, s_t=125, r=.1, n=2):
    f_0 = 0
    rate_period = r / n  # .05
    forward_price_0 = s_0 * (1 + rate_period) ** T
    forward_price_t = s_t * (1 + rate_period) ** (T - t)
    f_t = (forward_price_0 - forward_price_t) * calculateDiscountRate(t, T, rate_period)
    return -f_t

contractvalue_q7 = calculateCurrentValueOfForward()
print(contractvalue_q7)