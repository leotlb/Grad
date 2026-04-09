#include <iostream>
#include <cmath>

using namespace std;

const int MOD = 1000000007;
const int MOD_MINUS_1 = MOD - 1;


// Exponenciação binária aplicando a propriedade da multiplicação modular
// a.b congruente ((a mod p) . (b.mod p))mod p
long long mod_expo(long long base, long long exp, int mod) {
    long long result = 1;
    base = base % mod;
    
    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp >>= 1;
    }
    return result;
}


// Pelo pequeno teorema de Fermat para b^c com 0<c<p-1, temos valores diferentes aplicando mod p em b^c
// após disso os valores se repetem ciclicamente, logo b^c pode ser reduzido para b^c mod(p-1)
long long large_mod_expo(long long b, long long c, int mod_minus_1) {
    return mod_expo(b, c, mod_minus_1);
}


int main() {
    long long a, b, c;
    int cnt;

    cin >> cnt;

	for(int i = 0; i < cnt; i++){
		cin >> a >> b >> c;
		
		//b^c mod p-1
		long long exp = large_mod_expo(b, c, MOD_MINUS_1);
		
		//a^(b^c mod p-1)
		long long result = mod_expo(a, exp, MOD);
		
		cout << result << endl;
	}
    return 0;
}