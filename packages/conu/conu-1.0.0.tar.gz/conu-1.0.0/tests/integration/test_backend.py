# -*- coding: utf-8 -*-
#
# Copyright Contributors to the Conu project.
# SPDX-License-Identifier: MIT
#
import logging
import os
import pytest

from ..constants import FEDORA_MINIMAL_REPOSITORY, FEDORA_MINIMAL_REPOSITORY_TAG

from conu import DockerImage, DockerBackend
from conu.apidefs.backend import CleanupPolicy
from conu.backend.docker.client import get_client
from conu.fixtures import docker_backend


# FIXME: Remove xfail once https://github.com/user-cont/conu/issues/262 is fixed.
@pytest.mark.xfail(raises=AssertionError)
def test_cleanup_containers():
    with DockerBackend(logging_level=logging.DEBUG, cleanup=[CleanupPolicy.CONTAINERS]) as backend:
        # cleaning up from previous runs
        backend.cleanup_containers()

        client = get_client()
        container_sum = len(client.containers(all=True))
        image = DockerImage(FEDORA_MINIMAL_REPOSITORY, tag=FEDORA_MINIMAL_REPOSITORY_TAG)
        command = ["ls"]
        additional_opts = ["-i", "-t"]

        for i in range(3):
            image.run_via_binary(command=command, additional_opts=additional_opts)

        assert container_sum+3 == len(client.containers(all=True))

    assert container_sum == len(client.containers(all=True))


def test_standard_cleanup_tmpdir():
    with DockerBackend(cleanup=[CleanupPolicy.TMP_DIRS]) as backend:
        t = backend.tmpdir
        assert os.path.isdir(t)
    assert not os.path.isdir(t)


def test_non_cm_backend_tmpdir():
    from conu.apidefs.backend import get_backend_tmpdir

    b_tmp = get_backend_tmpdir()
    assert os.path.isdir(b_tmp)

    def scope():
        backend = DockerBackend(logging_level=logging.DEBUG)
        assert backend.tmpdir is None

    scope()
    assert os.path.isdir(b_tmp)
    b_tmp = get_backend_tmpdir()

    # test reinitialization
    with DockerBackend(logging_level=logging.DEBUG, cleanup=[CleanupPolicy.TMP_DIRS]) as b:
        t = b.tmpdir
        assert os.path.isdir(t)
        assert b_tmp == t

    assert not os.path.isdir(t)


def test_backend_fixture(docker_backend):
    assert isinstance(docker_backend, DockerBackend)
