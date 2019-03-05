import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_dependencies_are_installed(host):
    apt_transport_https = host.package('apt-transport-https')
    ca_certificates = host.package('ca-certificates')
    gnupg2 = host.package('gnupg2')
    software_properties_common = host.package('software-properties-common')

    assert apt_transport_https.is_installed
    assert ca_certificates.is_installed
    assert gnupg2.is_installed
    assert software_properties_common.is_installed


def test_docker_is_installed(host):
    docker_ce = host.package('docker-ce')

    assert docker_ce.is_installed


def test_docker_old_version_are_uninstalled(host):
    docker = host.package('docker')
    docker_engine = host.package('docker-engine')
    docker_io = host.package('docker.io')
    containerd = host.package('containerd')
    runc = host.package('runc')

    assert not docker.is_installed
    assert not docker_engine.is_installed
    assert not docker_io.is_installed
    assert not containerd.is_installed
    assert not runc.is_installed
