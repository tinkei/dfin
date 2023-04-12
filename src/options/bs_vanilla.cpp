#include <iostream>
#include <cmath>
#include <cassert>



double normal_cdf(const double& x) {
    return (1.0 + erf(x/sqrt(2.0))) / 2.0;
}

double call_price(const double& S, const double& K, const double& r, const double& t, const double& sigma) {
    double d1 = (log(S / K) + (r + 0.5*sigma*sigma)*t) / (sigma * sqrt(t));
    double d2 = d1 - sigma * sqrt(t);

    return S * (1.0 + erf(d1/sqrt(2.0))) / 2.0 - K * exp(-r*t) * (1.0 + erf(d2/sqrt(2.0))) / 2.0;
}

double put_price(const double& S, const double& K, const double& r, const double& t, const double& sigma) {
    double d1 = (log(S / K) + (r + 0.5*sigma*sigma)*t) / (sigma * sqrt(t));
    double d2 = d1 - sigma * sqrt(t);

    return K * exp(-r*t) * (1.0 + erf(-d2/sqrt(2.0))) / 2.0 - S * (1.0 + erf(-d1/sqrt(2.0))) / 2.0;
}



void test_call_price() {
    double S = 100.0;
    double K = 110.0;
    double r = 0.05;
    double t = 1.0;
    double sigma = 0.2;

    double expected_result = 6.040088129724;
    double tolerance = 0.001;

    double result = call_price(S, K, r, t, sigma);

    assert(abs(result - expected_result) < tolerance);
}

void test_put_price() {
    double S = 100.0;
    double K = 110.0;
    double r = 0.05;
    double t = 1.0;
    double sigma = 0.2;

    double expected_result = 10.675324824803;
    double tolerance = 0.001;

    double result = put_price(S, K, r, t, sigma);

    assert(abs(result - expected_result) < tolerance);
}



/*
int main() {
    double S = 100.0;
    double K = 110.0;
    double r = 0.05;
    double t = 1.0;
    double sigma = 0.2;

    std::cout << "Call price: $" << call_price(S, K, r, t, sigma) << std::endl;
    std::cout << "Put price : $" << put_price(S, K, r, t, sigma)  << std::endl;

    test_call_price();
    test_put_price();

    std::cout << "All tests passed!" << std::endl;

    return 0;
}
*/
