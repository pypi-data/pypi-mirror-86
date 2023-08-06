# -*- coding: utf-8 -*-
#
# Copyright Contributors to the Conu project.
# SPDX-License-Identifier: MIT
#
from __future__ import print_function, unicode_literals

import subprocess

import pytest

from conu import check_port, Probe
from conu.utils import s2i_command_exists, getenforce_command_exists, \
    chcon_command_exists, setfacl_command_exists, command_exists, CommandDoesNotExistException, \
    check_docker_command_works, run_cmd


def test_probes_port():
    port = 1234
    host = "127.0.0.1"
    probe = Probe(timeout=20, fnc=check_port, host=host, port=port)
    assert not check_port(host=host, port=port)

    bckgrnd = subprocess.Popen(["nc", "-l", str(port)], stdout=subprocess.PIPE)
    assert probe.run()
    assert not check_port(host=host, port=port)
    bckgrnd.kill()
    assert not check_port(host=host, port=port)

    subprocess.Popen(["nc", "-l", str(port)], stdout=subprocess.PIPE)
    assert probe.run()
    assert not check_port(host=host, port=port)


def test_required_binaries_exist():
    # should work since we have all the deps installed
    assert s2i_command_exists()
    assert getenforce_command_exists()
    assert chcon_command_exists()
    assert setfacl_command_exists()


def test_command_exists():
    m = "msg"
    command_exists("printf", ["printf", "--version"], m)
    with pytest.raises(CommandDoesNotExistException) as exc:
        command_exists("printof", ["printof", "--versionotron"], m)
        assert exc.value.msg == m


def test_check_docker():
    assert check_docker_command_works()


def test_run_cmd():
    ret = run_cmd(["sh", "-c", "for x in `seq 1 5`; do echo $x; sleep 0.01; done"])
    assert not ret

    ret = run_cmd(["sh", "-c", "for x in `seq 1 5`; do echo $x; sleep 0.01; done"],
                  return_output=True)
    assert ret == '1\n2\n3\n4\n5\n'

    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        ret = run_cmd(["sh", "-c", "exit 5"])
        assert not ret
    assert excinfo.value.returncode == 5

    ret = run_cmd(["sh", "-c", "exit 5"], ignore_status=True)
    assert ret == 5
