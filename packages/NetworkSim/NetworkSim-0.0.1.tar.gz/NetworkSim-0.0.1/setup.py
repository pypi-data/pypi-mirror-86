import setuptools

setuptools.setup(
    name="NetworkSim",
    version="0.0.1",
    license='MIT',
    author="Cheuk Ming Chung, Hongyi Yang",
    author_email="author@example.com",
    url="https://github.com/HYang1996/NetworkSim",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'simpy',
        'pandas'
      ],
)