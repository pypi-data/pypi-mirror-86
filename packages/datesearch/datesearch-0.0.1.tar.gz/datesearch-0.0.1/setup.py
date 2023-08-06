from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['pymorphy2==0.8', 'pymorphy2-dicts-ru==2.4.404381.4453942']

setup(
    name="datesearch",
    version="0.0.1",
    author="Evgeniy Blinov",
    author_email="zheni-b@yandex.ru",
    description="Поиск токенов, относящихся к датам, по регулярным выражениям",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pomponchik/datesearch",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
