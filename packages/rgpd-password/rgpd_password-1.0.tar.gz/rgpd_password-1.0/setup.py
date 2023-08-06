from setuptools import setup, find_packages

setup(
    name="rgpd_password",
    version="1.0",
    description="Tools to generate RGPD friendly password",
    author="Arthur RICHARD",
    packages=find_packages(),
    license="MIT",
    entry_points={
        "console_scripts": [
            "rgpd_gen=pwd_gen.randomize:generate_rgpd_password"
        ]
    }
)