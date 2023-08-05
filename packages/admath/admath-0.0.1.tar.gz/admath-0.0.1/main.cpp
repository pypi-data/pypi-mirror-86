#include <iostream>

#include <Python.h>
#include "info.h"
#include "prime.cpp"
#include "perAcom.cpp"

void version(){
	using namespace std;
	cout << MODULE_NAME << "-"
	<< VERSION << " by " << AUTHOR << endl;
}

/**
 * 对函数进行封装
 *
 * @param self
 * @param args
 * @return
 */
PyObject *
strings_reverse(PyObject *self, PyObject *args) {
	// 参数解析
	if (!PyArg_ParseTuple(args,"")) {
		return NULL;
	}
	version();
	return Py_BuildValue("");
}
 
/**
 * 定义模块方法表
 *
 */
static PyMethodDef AdMathMethods[] = {
		
		{"version",//在python里面使用的函数名:strings.reverse2(...)
		 strings_reverse,//python调用的c++的函数
		 METH_VARARGS, 
		 "输出高级数学库的版本信息"//python函数文档
		 },
		//{"pow2", c_pow, METH_VARARGS, "do pow"},
		{"isPrime", c_isPrime, METH_VARARGS, "判断一个整型是否为质数"},
		{"gcd", c_gcd, METH_VARARGS, "返回两个整形的最大公约数"},
		{"lcm", c_lcm, METH_VARARGS, "返回两个整形的最小公倍数"},
		{"factorial", c_factorial, METH_VARARGS, "无符号整型n的阶乘，注意容易溢出"},
		{"combine", c_combine, METH_VARARGS, "组合数C(n,k)"},
		{"permutation", c_permutation, METH_VARARGS, "排列数数A(n,k)"},
		{"getPrimeFactors", c_getPrimeFactors, METH_VARARGS, "分解质因子，返回元组"},
		
		{NULL, NULL, 0, NULL}
};
 
/**
 * 定义模块
 *
 */
static struct PyModuleDef admathmodule = {
		PyModuleDef_HEAD_INIT,
		"admath",
		"高级数学库",
		-1,
		AdMathMethods
};
 
/**
 * 模块初始化
 *
 * @return
 */
PyMODINIT_FUNC
PyInit_admath(void) {
	return PyModule_Create(&admathmodule);
}