from setuptools import setup

setup(name='delta_robot_trampoline',
      version='0.1.1',
      description='A Delta robot that bounces a soccer ball',
      url='https://github.com/RicoJia/delta_robot_trampoline',
      author='Rico Ruotong Jia',
      author_email='ruotongjia2020@u.northwestern.edu',
      license='BSD',
      install_requires=['numpy', 'pybullet'],
      packages=['delta_robot_trampoline'],
      zip_safe=False,
      python_requires='>=3')

