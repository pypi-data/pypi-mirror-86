# change these things before uploading (e.g. We are not stephen hudson)
from setuptools import setup

setup(
    name='capybaras',
    version='0.1.7',
    description='A example Python package',
    url='https://github.com/shuds13/pyexample',
    author='Stephen Hudson',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=['gpu_plus'],
    #package_data={'pre.txt':['gpu_plus/pre.txt'], 
    #    'post.txt':['gpu_plus/post.txt'],
    #    'pre_mouse.txt':['gpu_plus/pre_mouse.txt'],
    #    'post_mouse.txt':['gpu_plus/post_mouse.txt']},
    install_requires=['numpy', 'networkx', 'pyopencl', 'scipy', 'gpuinfo'],
    include_package_data=True, 

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
) 
