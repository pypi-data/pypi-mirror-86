import setuptools
 
with open('README.md', 'r') as fh:
	long_description = fh.read()
 
admath_module = setuptools.\
Extension('admath',
		sources=['main.cpp'
		],
		libraries=["info.h"],
		extra_link_args=['-Wl,-rpath=./'],#一定要加，让运行时候链接器知道去哪儿找文件
		include_dirs=['.'],
		library_dirs=['.'],
		language='c++')
 
setuptools.setup(
	name="admath",
	version="0.0.4",
	author="XYZboom",
	author_email="XYZboom@qq.com",
	description="高级数学库",
	long_description=long_description,
	long_description_content_type="text/markdown",
	#url="https://github.com/lpe234/strings_pkg",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	ext_modules=[admath_module]
)