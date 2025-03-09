# Save this file in '.py' extension

# Import required libraries
# Kannan Singaravelu : BS + IV
from numpy import *
import numpy as np
from scipy.stats import norm
from scipy.optimize import fsolve

# Black Scholes Option
class BS:
    """
    This is a class for Options contract for pricing European options on stocks/index without dividends.

    Attributes:
        spot       : int or float
        strike     : int or float
        rate       : float
        dte        : int or float (days to expiration in number of years)
        volatility : float
        callprice  : int or float (default None)
        putprice   : int or float (default None)
    """

    def __init__(self, spot, strike, rate, dte, volatility, callprice=None, putprice=None):
        # Spot Price
        self.spot = spot

        # Option Strike
        self.strike = strike

        # Interest Rate
        self.rate = rate

        # Days To Expiration
        self.dte = dte

        # Volatility
        self.volatility = volatility

        # Callprice = mkt price
        self.callprice = callprice

        # Putprice = mkt price
        self.putprice = putprice

        # Utility
        self._a = self.volatility * self.dte**0.5

        if self.strike == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            self._d1 = (log(self.spot / self.strike) + (self.rate + (self.volatility**2) / 2) * self.dte) / self._a

        self._d2 = self._d1 - self._a
        self._b = e**-(self.rate * self.dte)

        # The __dict__ attribute
        '''
        Contains all the attributes defined for the object itself. 
        It maps the attribute name to its value.
        '''
        for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', 
                'callTheta', 'putTheta', 'callRho', 'putRho', 
                'vega', 'gamma', 'impvol']:
            self.__dict__[i] = None

        [self.callPrice, self.putPrice] = self._price()
        [self.callDelta, self.putDelta] = self._delta()
        [self.callTheta, self.putTheta] = self._theta()
        [self.callRho, self.putRho] = self._rho()
        self.vega = self._vega()
        self.gamma = self._gamma()
        self.impvol = self._impvol()

    # Option Price
    def _price(self):
        '''Returns the option price: [Call price, Put price]'''
        if self.volatility == 0 or self.dte == 0:
            call = maximum(0.0, self.spot - self.strike)
            put = maximum(0.0, self.strike - self.spot)
        else:
            call = self.spot * norm.cdf(self._d1) - self.strike * e**(-self.rate * self.dte) * norm.cdf(self._d2)
            put = self.strike * e**(-self.rate * self.dte) * norm.cdf(-self._d2) - self.spot * norm.cdf(-self._d1)
        return [call, put]

    # Option Delta
    def _delta(self):
        '''Returns the option delta: [Call delta, Put delta]'''
        if self.volatility == 0 or self.dte == 0:
            call = 1.0 if self.spot > self.strike else 0.0
            put = -1.0 if self.spot < self.strike else 0.0
        else:
            call = norm.cdf(self._d1)
            put = -norm.cdf(-self._d1)
        return [call, put]

    # Option Gamma
    def _gamma(self):
        '''Returns the option gamma'''
        return norm.pdf(self._d1) / (self.spot * self._a)

    # Option Vega
    def _vega(self):
        '''Returns the option vega'''
        if self.volatility == 0 or self.dte == 0:
            return 0.0
        else:
            return self.spot * norm.pdf(self._d1) * self.dte**0.5 / 100
        
    # Option Theta
    def _theta(self):
        '''Returns the option theta: [Call theta, Put theta]'''
        call = -self.spot * norm.pdf(self._d1) * self.volatility / (2 * self.dte**0.5) - \
            self.rate * self.strike * self._b * norm.cdf(self._d2)
        
        put = -self.spot * norm.pdf(self._d1) * self.volatility / (2 * self.dte**0.5) + \
            self.rate * self.strike * self._b * norm.cdf(-self._d2)
        
        return [call / 365, put / 365]

    # Option Rho
    def _rho(self):
        '''Returns the option rho: [Call rho, Put rho]'''
        call = self.strike * self.dte * self._b * norm.cdf(self._d2) / 100
        put = -self.strike * self.dte * self._b * norm.cdf(-self._d2) / 100
        
        return [call, put]
        
    # Option Implied Volatility
    # Kannan Singaravelu: append base class with imp vol
    def _impvol(self):
        '''Returns the option implied volatility'''
        if (self.callprice or self.putprice) is None:
            return self.volatility
        else:
            def f(sigma):
                option = BS(self.spot, self.strike, self.rate, self.dte, sigma)
                if self.callprice:
                    return option.callPrice - self.callprice  # f(x) = BS_Call - MarketPrice
                if self.putprice and not self.callprice:
                    return option.putPrice - self.putprice

            return np.maximum(1e-5, np.real(fsolve(f, 0.2)[0]))
