from setuptools import setup, find_packages


setup(
    name='bounty-dork',
    version='0.0.1',
    url='https://github.com/ElNiak/BountyDork',
    description='Automated Google Dorking tool for pentesters without API keys.',
    long_description=open('README.md').read(),
    include_package_data=True,
    author='ElNiak',
    author_email='christophe.crochet@uclouvain.be',
    maintainer='ElNiak',
    maintainer_email='christophe.crochet@uclouvain.be',
    packages=find_packages(),
    package_data={'': ['bounty_dork/dorks/google/*.txt', 'bounty_dork/vpn_proxies/proxies/*.txt', 'bounty_dork/configs/*.txt']},
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development, Dorking, Bug Bounty, Google :: Libraries :: Python Modules',
    ],
)