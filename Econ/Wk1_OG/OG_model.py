import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

yrs_live = 60

S = 3

nvec = np.array([1.0, 1.0, 0.2])

alpha = 0.35

A = 1.0

delta_annual = 0.05

beta_annual = 0.96

delta = 1 - (1 - delta_annual) ** (yrs_live / S)

beta = beta_annual ** (yrs_live / S)

sigma = 3

SS_tol = 1e-13


#Solving for SS


def find_w(b2b3vals, nvec, A, alpha):
	return (1 - alpha) * A * ((sum(b2b3vals) / sum(nvec)) ** alpha)


def find_r(b2b3vals, nvec, A, alpha, delta):
	return alpha * A * ((sum(nvec) / sum(b2b3vals)) ** (1 - alpha)) - delta


def find_c1(b2b3vals, nvec, w):
	return nvec[0] * w - b2b3vals[0]


def find_c2(b2b3vals, nvec, w, r):
	return nvec[1] * w + (1 + r) * b2b3vals[0] - b2b3vals[1]


def find_c3(b2b3vals, nvec, w, r):
	return nvec[2] * w + (1 + r) * b2b3vals[1]


def MU_stitch(c, sigma):
	epsilon = 0.0001

	c_cnstr = c < epsilon

	if c_cnstr:
		b2 = (-sigma * (epsilon ** (-sigma - 1))) / 2
		b1 = (epsilon ** (-sigma)) - 2 * b2 * epsilon
		Mu_c = 2 * b2 * c + b1

	else:
		Mu_c = c ** (-sigma)

	return Mu_c


def error_finderSS(b2b3vals, nvec, A, alpha, delta, beta, sigma):

	w = find_w(b2b3vals, nvec, A, alpha)

	r = find_r(b2b3vals, nvec, A, alpha, delta)

	c1 = find_c1(b2b3vals, nvec, w)

	c2 = find_c2(b2b3vals, nvec, w, r)

	c3 = find_c3(b2b3vals, nvec, w, r)

	Mu_c1 = MU_stitch(c1, sigma)

	Mu_c2 = MU_stitch(c2, sigma)

	Mu_c3 = MU_stitch(c3, sigma)

	error1 = Mu_c1 - beta * (1 + r) * Mu_c2

	error2 = Mu_c2 - beta * (1 + r) * Mu_c3
	
	return np.array([error1, error2])


class Model(object):
	def __init__(self, nvec, A, alpha, delta, beta, sigma, SS_tol):
		self.nvec = nvec
		self.A = A
		self.alpha = alpha
		self.delta = delta
		self.beta = beta
		self.sigma = sigma
		self.SS_tol = SS_tol
		self.b2bar, self.b3bar = opt.root(error_finderSS, np.array([0.01, 0.01]), args=(
			nvec, A, alpha, delta, beta, sigma), tol=SS_tol).x
		self.b2barb3barvals = np.array([self.b2bar, self.b3bar])
		self.wbar = find_w(self.b2barb3barvals, nvec, A, alpha)
		self.rbar = find_r(self.b2barb3barvals, nvec, A, alpha, delta)
		self.c1bar = find_c1(self.b2barb3barvals, nvec, self.wbar)
		self.c2bar = find_c2(self.b2barb3barvals, nvec, self.wbar, self.rbar)
		self.c3bar = find_c3(self.b2barb3barvals, nvec, self.wbar, self.rbar)

	def __str__(self):
		return "b2bar = {}\nb3bar = {}\nwbar = {}\nrbar = {}\nc1bar = {}\nc2bar = {}\nc3bar = {}\n".format(self.b2bar, self.b3bar, self.wbar, self.rbar, self.c1bar, self.c2bar, self.c3bar)


print("For beta = 0.442, we get:\n")

beta1 = Model(nvec, A, alpha, delta, beta, sigma, SS_tol)

print(beta1)

print("For beta = 0.55, we get:\n")

beta2 = Model(nvec, A, alpha, delta, 0.55, sigma, SS_tol)

print(beta2)

print("We get that every steady state value increases, except for the interest rate r, which decreases.\n"
	"The intuition is that agents with higher patience will save more because they discount future consumption less,\n"
	"so they would rather save in the current period and consume their savings with interest in the next period rather than\n"
	"forgoing that interest by consuming in the current period. So, b2bar and b3bar increase, and thus K also increases.\n"
	"Since labor is exogenous and fixed, this increase in K leads to a decrease in rbar and an increase in wbar,\n"
	"due to the Inada conditions on the production function. Indeed, this increase in wbar is sufficiently large that\n"
	"c1bar increases along with b2bar. This combination of higher wages and higher savings allows c2bar to increase\n"
	"with b3bar despite the decrease in rbar. Finally, c3bar also increases despite the decrease in rbar.")

#Time Path Iteration:

b2SS, b3SS = beta1.b2bar, beta1.b3bar

b2new, b3new = 0.8 * b2SS, 1.1 * b3SS

T = 15

xsi = 0.15

TPI_tol = 1e-13

epsilon = 10e-9


def find_wvec(Kvec, nvec, A, alpha):
	wvec = []
	for K in Kvec:
		wvec.append((1 - alpha) * A * (K / sum(nvec)) ** alpha)
	return np.array(wvec)


def find_rvec(Kvec, nvec, A, alpha, delta):
	rvec = []
	for K in Kvec:
		rvec.append(alpha * A * ((sum(nvec) / K) ** (1 - alpha)) - delta)
	return np.array(rvec)


def error_finderTPI(b2b3vals, nvec, beta, sigma, w1, w2, w3, r2, r3):
	c1 = find_c1(b2b3vals, nvec, w1)

	c2 = find_c2(b2b3vals, nvec, w2, r2)

	c3 = find_c3(b2b3vals, nvec, w3, r3)

	Mu_c1 = MU_stitch(c1, sigma)

	Mu_c2 = MU_stitch(c2, sigma)

	Mu_c3 = MU_stitch(c3, sigma)

	error1 = Mu_c1 - beta * (1 + r2) * Mu_c2

	error2 = Mu_c2 - beta * (1 + r3) * Mu_c3

	return np.array([error1, error2])

def get_initialb3(b2new, nvec, beta, sigma, w2, w3, r2, r3):
	return (((beta * (1 + r3)) ** (1 / sigma)) * (nvec[1] * w2 + (1 + r2) * b2new) - nvec[2] * w3) / ((1 + r3) + ((beta * (1 + r3)) ** (1 / sigma)))
	
def find_b2b3vecs(wvec, rvec, nvec, beta, sigma, b2new, b3new, b2SS, TPI_tol):
	b3vec = [b3new, get_initialb3(b2new, nvec, beta, sigma, wvec[0], wvec[1], rvec[0], rvec[1])]
	b2vec = [b2new]
	for i in range(len(wvec) - 2):
		b2val, b3val = opt.root(error_finderTPI, np.array([0.01, 0.01]), args=(
					nvec, beta, sigma, wvec[i], wvec[i + 1], wvec[i + 2], rvec[i + 1], rvec[i + 2]), tol=TPI_tol).x
		b2vec.append(b2val)
		b3vec.append(b3val)
	b2vec.append(b2SS)
	return np.array(b2vec), np.array(b3vec)

def L_squared_norm(Kvec_previous, Kvec_next):
	return np.sum(np.divide(np.subtract(Kvec_previous, Kvec_next), Kvec_previous) ** 2)

def find_final_TP(nvec, beta, sigma, b2new, b3new, b2SS, b3SS, xsi, TPI_tol):
	Kvec_guess = np.append(np.linspace(b2new + b3new, b2SS + b3SS, T), b2SS + b3SS)
	Kvec_previous = Kvec_guess
	while True:
		wvec = find_wvec(Kvec_previous, nvec, A, alpha)
		rvec = find_rvec(Kvec_previous, nvec, A, alpha, delta)
		b2vec, b3vec = find_b2b3vecs(wvec, rvec, nvec, beta, sigma, b2new, b3new, b2SS, TPI_tol)
		Kvec_calculated = np.add(b2vec, b3vec)
		Kvec_next = np.add(xsi * Kvec_calculated, (1 - xsi) * Kvec_previous)
		if L_squared_norm(Kvec_previous, Kvec_next) < epsilon:
			return Kvec_next
		else:
			Kvec_previous = Kvec_next

K_TPI = np.hstack((find_final_TP(nvec, beta, sigma, b2new, b3new, b2SS, b3SS, xsi, TPI_tol), np.array([b2SS + b3SS] * 4)))

def T_finder(K_TPI, b2SS, b3SS):
	T = 0
	for (i, K) in enumerate(K_TPI):
		if abs(b2SS + b3SS - K) < 0.0001:
			if T == 0:
				T = i + 1
		else:
			T = 0
	return T

print("The real value of T is {}.".format(T_finder(K_TPI, b2SS, b3SS)))

plt.plot(range(1, T + 6), K_TPI)
plt.show()

#Guess T, period by which we reach SS (Try 30 or even 15)
#
#Guess time path for Kt from t = 1 to T s.t. K1 = b2,1 + b3,1, Kt = Kbar for all t >= T
#
#This gives you time paths for r and w since we know aggregate labor
#
#get_r(K, L, parameters):
#	return time path for r
#
#Now we can solve all households problems over the time path
#
#Now we can get the b2b3vals from t = 1 to T
#
#Use a sum of squared errors norm between K^iprime and K^i
#
#K^i + 1 = xiK^iprime + (1 - xi)K^i
#
#xi = 0.2 or something, between 0 and 1 and pretty small
#


