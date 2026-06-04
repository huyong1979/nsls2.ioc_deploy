import os

import pytest

DEVICE_ROLES = [
    role
    for role in os.listdir("roles/install_ioc/tasks/device_types")
    if os.path.isdir(os.path.join("roles/install_ioc/tasks/device_types", role))
]


@pytest.mark.parametrize("device_role", DEVICE_ROLES)
def test_ensure_var_file_for_device_role_exists(device_role):
    var_file_path = os.path.join("roles", "install_ioc", "tasks", "device_types", device_role, "vars.yml")
    assert os.path.exists(var_file_path), f"Vars file {var_file_path} not found"
