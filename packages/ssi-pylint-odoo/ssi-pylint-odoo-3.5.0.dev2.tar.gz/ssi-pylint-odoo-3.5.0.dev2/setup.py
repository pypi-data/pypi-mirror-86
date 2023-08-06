
import setuptools


setuptools.setup(setup_requires=['pbr'],
                 pbr=True,
                 test_suite="ssi_pylint_odoo.test",
                 package_data={'': ['*.yaml']})
