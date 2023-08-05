#include <vector>

#include <Python.h>

#include <cmath> 

#define VNAME(v) #v
#define PRINT(v) cout << VNAME(v) << ":" << (v) << endl;
#define LEN(a) (sizeof((a))/sizeof((a)[0]))
#define FOR(i,a,b) for(int i=(a);i<(b);++i)
#define FORR(i,a,b) for(int i=(a);i<=(b);++i)
typedef long long LL;
typedef unsigned long long LLU;

PyObject *
getPrimeFactors(LLU n){
	std::vector<LLU> s;
	int len = 0;
	for(LLU i=2;i<=sqrt(n);i++){
		while(!(n%i)){
			n/=i;
			s.push_back(i);
			len++;
		}
	}
	s.push_back(n);
	PyObject * r = PyTuple_New(++len);
	int r_c = 0;//s的下标（也是python对象r的下标）
	for(auto i=s.begin();i!=s.end();i++){
		PyTuple_SetItem(r,r_c++,Py_BuildValue("K", *i));
	}
	return r;
}

LL gcd(LL a,LL b){//最大公约数
	return a==0?b:gcd(b%a,a);
}
LL lcm(LL a,LL b){//最小公倍数
	return a*b/gcd(a,b);
}

PyObject * isPrime(LLU l) {//是否为质数
	if(l%2==0){
		return Py_False;//这个宏由python官方提供
	}
	for(int i=3;i<=sqrt(l);i+=2){
		if(l%i==0){
			return Py_False;
		}
	}
	return Py_True;
}
 
/**
 * 对函数进行封装
 *
 * @param self
 * @param args
 * @return
 */
PyObject *
c_isPrime(PyObject *self, PyObject *args) {
	LLU l;
 
	// 参数解析
	if (!PyArg_ParseTuple(args, "K", &l)) {
		return NULL;
	}
 
	// 调用 reverse
	PyObject * x = isPrime(l);
 
	return Py_BuildValue("O", x);
}
 
PyObject *
c_gcd(PyObject *self, PyObject *args) {
	LL a,b;
	// 参数解析
	if (!PyArg_ParseTuple(args, "LL", &a, &b)) {
		return NULL;
	}
	
	LL c = gcd(a,b);
	
	return Py_BuildValue("L", c);
}

PyObject *
c_lcm(PyObject *self, PyObject *args) {
	LL a,b;
	// 参数解析
	if (!PyArg_ParseTuple(args, "LL", &a, &b)) {
		return NULL;
	}
	
	LL c = lcm(a,b);
	
	return Py_BuildValue("L", c);
}


PyObject *
c_getPrimeFactors(PyObject *self, PyObject *args) {
	LLU l;
 
	// 参数解析
	if (!PyArg_ParseTuple(args, "K", &l)) {
		return NULL;
	}
 
	// 调用 reverse
	PyObject * x = getPrimeFactors(l);
 
	return Py_BuildValue("O", x);
}

