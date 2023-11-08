


from setuptools import setup


setup(
    name='fast_add_device',
    version='0.1.1',
    description='Scan device by ip',
    long_description='Scan device by ip for add new devices',
    long_description_content_type='text',
    author='Stepanov Evgeniy',
    author_email='jacksontur@yandex.ru',
    license='Nginx',
    install_requires=[],
    packages=["fast_add_device"],
    package_data={"fast_add_device": ["templates/fast_add_device/*.html"]},
    zip_safe=False
)


