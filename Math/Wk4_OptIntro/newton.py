def newton(x_0, epsilon, f_prime, f_double_prime):
	count = 0
	while True:
		if f_double_prime(x_0) == 0:
			raise ValueError('The sequence does not converge since f_double_prime(x_{}) = 0'.format(count))
		if x_0 == 0:
			raise ValueError('The sequence does not converge since x_{} = 0'.format(count))
		if count == 100000:
			raise ValueError('The sequence has not converged in 100000 iterations.')
		x_1 = x_0 - (f_prime(x_0) / f_double_prime(x_0))
		if abs(x_1 - x_0) < abs(x_0) * epsilon:
			return x_1
		x_0 = x_1
		count += 1