from Cython.Distutils import build_ext
import setuptools
import numpy

setuptools.setup(
    name='simple_camera',
    version='0.2.5',
    author="Dmitry Kostyaev",
    author_email="dm.kostyaev@gmail.com",
    url="https://github.com/kostyaev/simple_camera",
    cmdclass={'build_ext': build_ext},
    ext_modules=[setuptools.Extension("simple_camera.mesh_core_cython",
                                      sources=["simple_camera/lib/mesh_core_cython.pyx",
                                               "simple_camera/lib/mesh_core.cpp"],
                                      language='c++',
                                      include_dirs=[numpy.get_include()])],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['simple_camera']
)
