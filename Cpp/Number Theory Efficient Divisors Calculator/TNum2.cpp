#include <iostream>
#include <cstdio>
#include <bitset>
#include <vector>
#include <map>
#include <cmath>

using namespace std;

typedef long long ll;
typedef vector<int> vi;
typedef vector<ll> vll;
typedef map<int,int> mpi;
ll tamCrivo;


bitset<100001> crivo;
vll primos;

void crivoErastotenes(ll M){
	tamCrivo = M+1;
	crivo.set();

	crivo[0] = crivo[1] = 0;

	for (ll i = 2; i <= tamCrivo; ++i){
		if (crivo[i]){
			for (ll j = i*i; j <= tamCrivo; j += i)
				crivo[j]=0;
			primos.push_back(i);
		}
	}
}


map<int, int> primeFactorization(int n) {
    mpi factors;
    
    for (int prime : primos) {
        if (prime * prime > n) break;

        while (n % prime == 0) {
            factors[prime]++;
            n /= prime;
        }
    }
	
    if (n > 1) {
        factors[n]++;
    }

    return factors;
}

vi divisors(const mpi& factors){
    vi divisors = {1};
	
	for (const auto& factor : factors) {
        int prime = factor.first;
        int exponent = factor.second;

        vi current_divisors;
        for (int i = 0; i <= exponent; ++i) {
            for (int d : divisors) {
                current_divisors.push_back(d * pow(prime, i));
            }
        }
        divisors = current_divisors;
    }

    return divisors;
}


int main(int argc, char const *argv[]){
	
	int n,number;
	
	cin >> n;
	
	crivoErastotenes(100000);
	
	for(int i = 0; i < n; i++){
	    vi div;
	    mpi factors;
	    
	    cin >> number;
	    
	    factors = primeFactorization(number);
	    div = divisors(factors);
	    
	    cout << div.size() << endl;
	}

	return 0;
}