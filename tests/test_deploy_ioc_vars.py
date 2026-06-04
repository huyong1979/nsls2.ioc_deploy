import os

import pytest
import yamale
import yaml

INSTALL_IOC_VARS_FILES = [
    d
    for d in os.listdir("roles/install_ioc/tasks/device_types")
    if os.path.isdir(os.path.join("roles/install_ioc/tasks/device_types", d))
    and os.path.exists(os.path.join("roles/install_ioc/tasks/device_types", d, "vars.yml"))
]

INSTALL_MODULE_FILES = [
    os.path.splitext(f)[0]
    for f in os.listdir("roles/install_module/vars")
    if f.endswith(".yml")
]


pytestmark = pytest.mark.parametrize(
    "install_ioc_var_file", INSTALL_IOC_VARS_FILES, indirect=True
)


def test_install_ioc_var_file_has_matching_role(install_ioc_var_file):
    assert os.path.exists(os.path.join("roles/install_ioc/tasks/device_types", install_ioc_var_file.name))


def test_install_ioc_var_files_valid(install_ioc_var_file, module_name_validator):
    if install_ioc_var_file.data:
        data = yamale.make_data(content=yaml.dump(install_ioc_var_file.data))
        validators = yamale.validators.DefaultValidators.copy()
        validators["module_name"] = module_name_validator
        schema = yamale.make_schema(
            "schemas/device_specific_vars.yml", validators=validators
        )
        try:
            yamale.validate(schema, data)
        except Exception as e:
            pytest.fail(f"YAML validation failed: {e}")


def test_install_ioc_var_file_required_module_exists(install_ioc_var_file):
    if (
        install_ioc_var_file.data
        and "install_ioc_required_module" in install_ioc_var_file.data
    ):
        if install_ioc_var_file.data["install_ioc_required_module"]:
            assert os.path.exists(
                os.path.join(
                    "roles/install_module/vars",
                    f"{install_ioc_var_file.data['install_ioc_required_module']}.yml",
                )
            )
