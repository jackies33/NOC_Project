



from setuptools import setup



setup(
    name='ip_scan',
    version='0.1.1',
    description='Scan device by ip',
    long_description='Scan device by ip for add new devices',
    long_description_content_type='text',
    author='Stepanov Evgeniy',
    author_email='jacksontur@yandex.ru',
    license='Nginx',
    install_requires=[],
    packages=["ip_scan"],
    package_data={"ip_scan": ["templates/*.html"]},
    zip_safe=False
)


