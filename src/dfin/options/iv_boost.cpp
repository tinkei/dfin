#include <iostream>
#include <tuple>
#include <limits>
#include <cassert>

#include <boost/math/tools/roots.hpp>

#include "bs_vanilla.h"
// #include "newton_raphson.h"



double call_implied_volatility(const double& S, const double& K, const double& r, const double& t, const double& price) {
    auto f = [=](double sigma) {
        // const double epsilon = std::numeric_limits<double>::epsilon();
        // double zeroth = call_price(S, K, r, t, sigma) - price;
        // double first = (call_price(S, K, r, t, sigma + 10*epsilon) - call_price(S, K, r, t, sigma - 10*epsilon)) / 2.0 / 10.0 /epsilon;
        // std::tuple<double, double> result = std::make_tuple(zeroth, first);
        // double second = (call_price(S, K, r, t, sigma + 10*epsilon) - 2.0 * call_price(S, K, r, t, sigma) + call_price(S, K, r, t, sigma - 10*epsilon)) / epsilon / epsilon / 100;
        // std::tuple<double, double, double> result = std::make_tuple(zeroth, first, second);
        // return result;
        return call_price(S, K, r, t, sigma) - price;
    };
    double sigma_guess = 0.5;
    double min_sigma = 0.0;
    double max_sigma = 10.0;
    // int digits_accuracy = std::numeric_limits<double>::digits;
    // double implied_vol = newton_raphson_iterate(f, sigma_guess, min_sigma, max_sigma, digits_accuracy, UINT64_MAX);
    // double implied_vol = boost::math::tools::newton_raphson_iterate(f, sigma_guess, min_sigma, max_sigma, digits_accuracy);
    std::uintmax_t max_iter = 100000;
    std::pair<double, double> result = boost::math::tools::toms748_solve(f, min_sigma, max_sigma, boost::math::tools::eps_tolerance<double>(), max_iter);
    double implied_vol = (std::get<0>(result) + std::get<1>(result)) * 0.5;
    // std::cout << "Interval: " << std::get<0>(result) << " " << std::get<1>(result) << std::endl;
    return implied_vol;
}

double put_implied_volatility(const double& S, const double& K, const double& r, const double& t, const double& price) {
    auto f = [=](double sigma) {
        // const double epsilon = std::numeric_limits<double>::epsilon();
        // double zeroth = put_price(S, K, r, t, sigma) - price;
        // double first = (put_price(S, K, r, t, sigma + 10*epsilon) - put_price(S, K, r, t, sigma - 10*epsilon)) / 2.0 / 10.0 /epsilon;
        // std::tuple<double, double> result = std::make_tuple(zeroth, first);
        // double second = (put_price(S, K, r, t, sigma + 10*epsilon) - 2.0 * put_price(S, K, r, t, sigma) + put_price(S, K, r, t, sigma - 10*epsilon)) / epsilon / epsilon / 100;
        // std::tuple<double, double, double> result = std::make_tuple(zeroth, first, second);
        // return result;
        return put_price(S, K, r, t, sigma) - price;
    };
    double sigma_guess = 0.5;
    double min_sigma = 0.0;
    double max_sigma = 10.0;
    // int digits_accuracy = std::numeric_limits<double>::digits;
    // double implied_vol = newton_raphson_iterate(f, sigma_guess, min_sigma, max_sigma, digits_accuracy, UINT64_MAX);
    // double implied_vol = boost::math::tools::newton_raphson_iterate(f, sigma_guess, min_sigma, max_sigma, digits_accuracy);
    std::uintmax_t max_iter = 100000;
    std::pair<double, double> result = boost::math::tools::toms748_solve(f, min_sigma, max_sigma, boost::math::tools::eps_tolerance<double>(), max_iter);
    double implied_vol = (std::get<0>(result) + std::get<1>(result)) * 0.5;
    // std::cout << "Interval: " << std::get<0>(result) << " " << std::get<1>(result) << std::endl;
    return implied_vol;
}



void test_call_implied_volatility() {
    double S = 100.0;
    double K = 110.0;
    double r = 0.05;
    double t = 1.0;
    double price = 6.040088129724;

    double expected_result = 0.2;
    double tolerance = 0.001;

    double result = call_implied_volatility(S, K, r, t, price);

    assert(abs(result - expected_result) < tolerance);
}

void test_put_implied_volatility() {
    double S = 100.0;
    double K = 110.0;
    double r = 0.05;
    double t = 1.0;
    double price = 10.675324824803;

    double expected_result = 0.2;
    double tolerance = 0.001;

    double result = put_implied_volatility(S, K, r, t, price);

    assert(abs(result - expected_result) < tolerance);
}



int main() {

    auto f0 = [](double x) { return x*x - 2; };
    auto f1 = [](double x) { return std::tuple<double, double>(x*x - 2, 2*x); };
    auto f2 = [](double x) { return std::tuple<double, double, double>(x*x - 2, 2*x, 2); };
    double x0 = 1.5;
    double xmin = 0.0;
    double xmax = 3.0;
    int digits_accuracy = std::numeric_limits<double>::digits;
    // double root = newton_raphson_iterate(f1, x0, xmin, xmax, digits_accuracy, UINT64_MAX);
    double root = boost::math::tools::newton_raphson_iterate(f1, x0, xmin, xmax, digits_accuracy);
    std::cout << "Root 2: " << root << std::endl;

    double S = 100.0;
    double K = 110.0;
    double r = 0.05;
    double t = 1.0;
    double C = 6.040088129724;
    double P = 10.675324824803;
    double call_sigma = call_implied_volatility(S, K, r, t, C);
    std::cout << "Call implied volatility: " << call_sigma << std::endl;
    double put_sigma = put_implied_volatility(S, K, r, t, P);
    std::cout << "Put implied volatility: " << put_sigma << std::endl;

    test_call_price();
    test_put_price();
    test_call_implied_volatility();
    test_put_implied_volatility();

    std::cout << "All tests passed!" << std::endl;

    return 0;

}
