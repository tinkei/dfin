#ifndef BSIV_BOOST_H
#define BSIV_BOOST_H

double call_implied_volatility(const double& S, const double& K, const double& r, const double& t, const double& price);

double put_implied_volatility(const double& S, const double& K, const double& r, const double& t, const double& price);

void test_call_implied_volatility();

void test_put_implied_volatility();

#endif // BSIV_BOOST_H