# -*- coding: utf-8 -*-
#
# Copyright Contributors to the Conu project.
# SPDX-License-Identifier: MIT
#

"""
This is backend for podman engine
"""
import logging
import json
import re

from conu.apidefs.backend import Backend
from conu.backend.podman.container import PodmanContainer
from conu.backend.podman.image import PodmanImage, PodmanImagePullPolicy
from conu.backend.podman.constants import CONU_ARTIFACT_TAG

from conu.exceptions import ConuException

from conu.utils import run_cmd, parse_reference

logger = logging.getLogger(__name__)


class PodmanBackend(Backend):
    """
    For more info on using the Backend classes, see documentation of
    the parent :class:`conu.apidefs.backend.Backend` class.
    """
    name = "podman"
    ContainerClass = PodmanContainer
    ImageClass = PodmanImage

    def __init__(self, logging_level=logging.INFO, logging_kwargs=None, cleanup=None):
        """
        This method serves as a configuration interface for conu.

        :param logging_level: int, control logger verbosity: see logging.{DEBUG,INFO,ERROR}
        :param logging_kwargs: dict, additional keyword arguments for logger set up, for more info
                                see docstring of set_logging function
        :param cleanup: list, list of cleanup policy values, examples:
            - [CleanupPolicy.EVERYTHING]
            - [CleanupPolicy.VOLUMES, CleanupPolicy.TMP_DIRS]
            - [CleanupPolicy.NOTHING]
        """
        super(PodmanBackend, self).__init__(
            logging_level=logging_level, logging_kwargs=logging_kwargs, cleanup=cleanup)
        # we support podman-0.11+
        podman_version = self.get_version()
        if podman_version:
            try:
                maj, min, _ = podman_version
                maj, min = int(maj), int(min)
            except ValueError:
                logger.error("unable to parse major and minor part of podman version")
            else:
                if (0, 11) > (maj, min):
                    raise ConuException("We support podman from version 0.11, please update.")
        else:
            logger.warning("unable to parse version of podman, you're on your own")

    def get_version(self):
        """
        return 3-tuple of version info or None

        :return: (str, str, str)
        """
        raw_version = run_cmd(["podman", "version"], return_output=True)
        regex = re.compile(r"Version:\s*(\d+)\.(\d+)\.(\d+)")
        match = regex.findall(raw_version)
        try:
            return match[0]
        except IndexError:
            logger.error("unable to parse version from `podman version`")
            return

    def cleanup_containers(self):
        # TODO: Test this
        conu_containers = self._list_podman_containers(filter=CONU_ARTIFACT_TAG)
        for c in conu_containers:
            logger.info("Trying to remove conu container: %s" % c)
            logger.debug("Removing container %s created by conu", c)
            run_cmd(["podman", "stop", c])
            run_cmd(["podman", "rm", c])

    def list_containers(self):
        """
        List all available podman containers.

        :return: collection of instances of :class:`conu.PodmanContainer`
        """
        containers = []
        for container in self._list_podman_containers():
            identifier = container["ID"]
            name = container["Names"]
            image_name = container["Image"]

            try:
                image_name, image_tag = parse_reference(image_name)
            except (IndexError, TypeError):
                image_name, image_tag = None, None

            image = PodmanImage(image_name, tag=image_tag, identifier=None)
            container = PodmanContainer(image, identifier, name=name)
            containers.append(container)

        return containers

    def list_images(self):
        """
        List all available podman images.

        :return: collection of instances of :class:`conu.PodmanImage`
        """
        images = []
        for image in self._list_all_podman_images():
            try:
                i_name, tag = parse_reference(image["names"][0])
            except (IndexError, TypeError):
                i_name, tag = None, None
            d_im = PodmanImage(i_name, tag=tag, identifier=image["id"],
                               pull_policy=PodmanImagePullPolicy.NEVER)
            images.append(d_im)

        return images

    @staticmethod
    def _list_all_podman_images():
        """
        Finds all podman containers
        :return: list of dicts with image info
        """
        cmdline = ["podman", "images", "--format", "json"]
        output = run_cmd(cmdline, return_output=True)
        images = json.loads(output)
        return images

    @staticmethod
    def _list_podman_containers(filter=None):
        """
        Finds podman containers by filter or all containers
        :return: list of dicts with containers info
        """
        option = ["--filter", filter] if filter else ["-a"]
        cmdline = ["podman", "ps"] + option + ["--format", "json"]
        output = run_cmd(cmdline, return_output=True)
        containers = json.loads(output)
        return containers

    @staticmethod
    def _podman_command(args):
        """
        return podman command with default args to run

        :param args: list of str, arguments and options passed to podman binary
        :return: list of podman command and default args
        """
        return ["podman"] + args
