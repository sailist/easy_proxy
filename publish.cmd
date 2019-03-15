python setup.py sdist bdist_wheel
twine upload dist/*
rem twine upload --skip-existing dist/*