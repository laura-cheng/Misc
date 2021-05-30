#define wiwihorz
#include <bits/stdc++.h>
#pragma GCC optimize("Ofast")
#pragma loop-opt(on)

#define rep(i, a, b) for(int i = a; i <= b; i++)
#define rrep(i, a, b) for(int i = b; i >= a; i--)
#define all(x) x.begin(), x.end()
#define int long long int
using namespace std;
#ifdef wiwihorz
#define print(a...) kout("[" + string(#a) + "] = ", a)
void vprint(auto L, auto R) { while(L < R) cerr << *L << " \n"[next(L) == R], ++L;}
void kout() { cerr << endl; }
template<class T1, class ... T2> void kout(T1 a, T2 ... e) { cerr << a << " ", kout(e...);}
#else
#define print(...) 0
#define vprint(...) 0
#endif


namespace solver {
	string solve(string s, int id) {
		vector<int> keys;
		rep(i, 0, 3) {
			keys.push_back(id % 96);
			id /= 96;
		}
		string ans = "";
		for(int i = 0; i < s.size(); i += 4) {
			rrep(j, 1, 4) {
				int ch = (s[i + j - 1] - keys[4 - j] + 64 + 96) % 96;
				ans += char(ch + 32);
			}
		}
		return ans;
	}

};
using namespace solver;
signed main() {
	ios::sync_with_stdio(false), cin.tie(0);
	string s = "=Js&;*A`odZHi'>D=Js&#i-DYf>Uy'yuyfyu<)Gu";
	rep(i, 0, 84934656) {
		string ans = solve(s, i);
		if(ans.substr(0, 4) == "AIS3") {
			print(i, ans);
		}
	}
	return 0;
}
