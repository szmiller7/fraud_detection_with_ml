from setuptools import find_packages, setup


def get_requirements(file_path:str)->list[str]:
    """
    function returning list of requirements
    """
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        # remove escape character 
        requirements = [req.replace("\n", "") for req in requirements]
        # remove "-e ." from the requirements 
        e_dot = "-e ."
        if e_dot in requirements:
            requirements.remove(e_dot)


setup(
    name = "mlproject",
    version = "0.0.1",
    author = "Szymon Miller",
    author_email = "sz.miller7@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt"))

