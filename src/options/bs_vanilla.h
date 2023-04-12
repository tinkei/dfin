#ifndef BS_VANILLA_H
#define BS_VANILLA_H

double normal_cdf(const double& x);

double call_price(const double& S, const double& K, const double& r, const double& t, const double& sigma);

double put_price(const double& S, const double& K, const double& r, const double& t, const double& sigma);

void test_call_price();

void test_put_price();

#endif // BS_VANILLA_H