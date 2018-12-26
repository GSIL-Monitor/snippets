class Complex {
	friend bool operator==(const Complex& a, const Complex& b);
	double real, imaginary;
public:
	Complex(double r, double i = 0);
};
