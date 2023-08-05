//排列组合
#include <Python.h>

#include <cmath> 

#define VNAME(v) #v
#define PRINT(v) cout << VNAME(v) << ":" << (v) << endl;
#define LEN(a) (sizeof((a))/sizeof((a)[0]))
#define FOR(i,a,b) for(int i=(a);i<(b);++i)
#define FORR(i,a,b) for(int i=(a);i<=(b);++i)

typedef long long LL;
typedef unsigned long long LLU;

LLU factorial(LLU);

LLU permutation(LLU n,LLU k){//排列数
	return factorial(n)/factorial(n-k);
}

LLU combine(LLU n,LLU k){//组合数
	return factorial(n)/(factorial(k)*factorial(n-k));
}

LLU factorial(LLU l) {//阶乘
	if(l==0){
		return 1;
	}
	LLU r = 1;
	FORR(i,1,l){
		r *= i;
	}
	return r;
}
 
/**
 * 对函数进行封装
 *
 * @param self
 * @param args
 * @return
 */
PyObject *
c_permutation(PyObject *self, PyObject *args) {
	LLU n,k;
 
	// 参数解析
	if (!PyArg_ParseTuple(args, "KK", &n,&k)) {
		return NULL;
	}
	if(n<k){
		PyErr_SetString(PyExc_ValueError, "排列数数C(n,k)里，n不能小于k！");
		return NULL;
	}
	// 调用 reverse
	LLU x = permutation(n,k);
 
	return Py_BuildValue("L", x);
}

PyObject *
c_combine(PyObject *self, PyObject *args) {
	LLU n,k;
 
	// 参数解析
	if (!PyArg_ParseTuple(args, "KK", &n,&k)) {
		return NULL;
	}
	if(n<k){
		PyErr_SetString(PyExc_ValueError, "组合数C(n,k)里，n不能小于k！");
		return NULL;
	}
	// 调用 reverse
	LLU x = combine(n,k);
 
	return Py_BuildValue("L", x);
}

PyObject *
c_factorial(PyObject *self, PyObject *args) {
	LLU l;
 
	// 参数解析
	if (!PyArg_ParseTuple(args, "K", &l)) {//K:c++里面的LLU
		return NULL;
	}
 
	// 调用 reverse
	LLU x = factorial(l);
 
	return Py_BuildValue("L", x);
}







