import setuptools

long_description = '''This package defines Win32 virtual-key (VK) codes
                      for use on other platforms. In addition to constants,
                      the dictionaries `code_to_name` and `name_to_code`
                      are provided for programmatic conversion.'''

setuptools.setup(
    name='virtualkeys',
    packages=['virtualkeys'],
    version='0',
    author='biqqles',
    author_email='biqqles@protonmail.com',
    description='Cross-platform Win32 virtual-key codes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gist.github.com/biqqles/31d1611d23e76b0b7c59d203c0004798',
)
