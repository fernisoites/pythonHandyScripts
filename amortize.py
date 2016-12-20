def calculateRes(residual, mPay, mRate):
	interest = residual * mRate
	return residual + interest - mPay

def calculateDiff(owe, mPay, mRate):
	for _ in range(360):
		owe = calculateRes(owe, mPay, mRate)
	return owe

def main():
	price, yRate = 570000, 0.0425

	mRate = yRate/12
	owe = price * 0.8

	start, end = owe/360.0, (owe/360.0)* (1+mRate)**360
	epsilon = 0.000001
	while end - start > epsilon:
		mid = (start + end) / 2
		result = calculateDiff(owe, mid, mRate)
		if result < 0:
			end = mid
		elif result > 0:
			start = mid
		else:
			break

	print "{:.2f}".format(mid), "{:.2f}".format(mid * 360)

if __name__ == "__main__":
	main()