# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2018, 2019 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""REANA-DB utils."""

import os
from uuid import UUID

from sqlalchemy import inspect


def build_workspace_path(user_id, workflow_id=None):
    """Build user's workspace relative path.

    :param user_id: Owner of the workspace.
    :param workflow_id: Optional parameter, if provided gives the path to the
        workflow workspace instead of just the path to the user workspace.
    :return: String that represents the workspace relative path.
        i.e. users/0000/workflows/0034
    """
    workspace_path = os.path.join("users", str(user_id), "workflows")
    if workflow_id:
        workspace_path = os.path.join(workspace_path, str(workflow_id))

    return workspace_path


def _get_workflow_with_uuid_or_name(uuid_or_name, user_uuid):
    """Get Workflow from database with uuid or name.

    :param uuid_or_name: String representing a valid UUIDv4 or valid
        Workflow name. Valid name contains only ASCII alphanumerics.

        Name might be in format 'reana.workflow.123' with arbitrary
        number of dot-delimited substrings, where last substring specifies
        the run number of the workflow this workflow name refers to.

        If name does not contain a valid run number, but it is a valid name,
        workflow with latest run number of all the workflows with this name
        is returned.
    :type uuid_or_name: String

    :rtype: reana-db.models.Workflow
    """
    from reana_db.models import Workflow

    # Check existence
    if not uuid_or_name:
        raise ValueError("No Workflow was specified.")

    # Check validity
    try:
        uuid_or_name.encode("ascii")
    except UnicodeEncodeError:
        # `workflow_name` contains something else than just ASCII.
        raise ValueError("Workflow name {} is not valid.".format(uuid_or_name))

    # Check if UUIDv4
    try:
        # is_uuid = UUID(uuid_or_name, version=4)
        is_uuid = UUID("{" + uuid_or_name + "}", version=4)
    except (TypeError, ValueError):
        is_uuid = None

    if is_uuid:
        # `uuid_or_name` is an UUIDv4.
        # Search with it since it is expected to be unique.
        return _get_workflow_by_uuid(uuid_or_name)

    else:
        # `uuid_or_name` is not and UUIDv4. Expect it is a name.

        # Expect name might be in format 'reana.workflow.123' with arbitrary
        # number of dot-delimited substring, where last substring specifies
        # the run_number of the workflow this workflow name refers to.

        # Possible candidates for names are e.g. :
        # 'workflow_name' -> ValueError
        # 'workflow.name' -> True, True
        # 'workflow.name.123' -> True, True
        # '123.' -> True, False
        # '' -> ValueError
        # '.123' -> False, True
        # '..' -> False, False
        # '123.12' -> True, True
        # '123.12.' -> True, False

        # Try to split the dot-separated string.
        try:
            workflow_name, run_number = uuid_or_name.split(".", maxsplit=1)
        except ValueError:
            # Couldn't split. Probably not a dot-separated string.
            #  -> Search with `uuid_or_name`
            return _get_workflow_by_name(uuid_or_name, user_uuid)

        # Check if `run_number` was specified
        if not run_number:
            # No `run_number` specified.
            # -> Search by `workflow_name`
            return _get_workflow_by_name(workflow_name, user_uuid)

        # `run_number` was specified.
        # Check `run_number` is valid.
        try:
            run_number = float(run_number)
        except ValueError:
            # `uuid_or_name` was split, so it is a dot-separated string
            # but it didn't contain a valid `run_number`.
            # Assume that this dot-separated string is the name of
            # the workflow and search with it.
            return _get_workflow_by_name(uuid_or_name, user_uuid)

        # `run_number` is valid.
        # Search by `run_number` since it is a primary key.
        workflow = Workflow.query.filter(
            Workflow.name == workflow_name,
            Workflow.run_number == run_number,
            Workflow.owner_id == user_uuid,
        ).one_or_none()
        if not workflow:
            raise ValueError(
                "REANA_WORKON is set to {0}, but "
                "that workflow does not exist. "
                "Please set your REANA_WORKON environment "
                "variable appropriately.".format(workflow_name)
            )

        return workflow


def _get_workflow_by_name(workflow_name, user_uuid):
    """From Workflows named as `workflow_name` the latest run_number.

    Only use when you are sure that workflow_name is not UUIDv4.

    :rtype: reana-db.models.Workflow
    """
    from reana_db.models import Workflow

    workflow = (
        Workflow.query.filter(
            Workflow.name == workflow_name, Workflow.owner_id == user_uuid
        )
        .order_by(Workflow.run_number.desc())
        .first()
    )
    if not workflow:
        raise ValueError(
            "REANA_WORKON is set to {0}, but "
            "that workflow does not exist. "
            "Please set your REANA_WORKON environment "
            "variable appropriately.".format(workflow_name)
        )
    return workflow


def _get_workflow_by_uuid(workflow_uuid):
    """Get Workflow with UUIDv4.

    :param workflow_uuid: UUIDv4 of a Workflow.
    :type workflow_uuid: String representing a valid UUIDv4.

    :rtype: reana-db.models.Workflow
    """
    from reana_db.models import Workflow

    workflow = Workflow.query.filter(Workflow.id_ == workflow_uuid).first()
    if not workflow:
        raise ValueError(
            "REANA_WORKON is set to {0}, but "
            "that workflow does not exist. "
            "Please set your REANA_WORKON environment "
            "variable appropriately.".format(workflow_uuid)
        )
    return workflow


def get_default_quota_resource(resource_type):
    """
    Get default quota resource by given resource type.

    :param resource_type: Resource type corresponding to default resource to get.
    :type resource_type: reana_db.models.ResourceType
    """
    from reana_db.config import DEFAULT_QUOTA_RESOURCES
    from reana_db.models import Resource

    if resource_type not in DEFAULT_QUOTA_RESOURCES.keys():
        raise Exception(
            "Default resource of type {} does not exist.".format(resource_type)
        )

    return Resource.query.filter_by(name=DEFAULT_QUOTA_RESOURCES[resource_type]).one()


def update_users_disk_quota(user=None, bytes_to_sum=None):
    """Update users disk quota usage.

    :param user: User whose disk quota will be updated. If None, applies to all users.
    :param bytes_to_sum: Amount of bytes to sum to user disk quota,
        if None, `du` will be used to recalculate it.

    :type user: reana_db.models.User
    :type bytes_to_sum: int

    """
    from reana_commons.utils import get_disk_usage

    from reana_db.config import DEFAULT_QUOTA_RESOURCES
    from reana_db.models import Resource, User, UserResource

    users = [user] if user else User.query.all()

    for u in users:
        disk_resource = Resource.query.filter_by(
            name=DEFAULT_QUOTA_RESOURCES["disk"]
        ).one_or_none()

        if disk_resource:
            from .database import Session

            user_resource_quota = UserResource.query.filter_by(
                user_id=u.id_, resource_id=disk_resource.id_
            ).first()
            if bytes_to_sum:
                user_resource_quota.quota_used += bytes_to_sum
            else:
                workspace_path = u.get_user_workspace()
                disk_usage_bytes = get_disk_usage(workspace_path, summarize=True)
                disk_usage_bytes = int(disk_usage_bytes[0]["size"]["raw"])
                user_resource_quota.quota_used = disk_usage_bytes
            Session.commit()


def store_workflow_disk_quota(workflow, bytes_to_sum=None):
    """
    Update or create disk workflow resource.

    :param workflow: Workflow whose disk resource usage must be calculated.
    :param bytes_to_sum: Amount of bytes to sum to workflow disk quota,
        if None, `du` will be used to recalculate it.

    :type workflow: reana_db.models.Workflow
    :type bytes_to_sum: int
    """
    from reana_commons.errors import REANAMissingWorkspaceError
    from reana_commons.utils import get_disk_usage

    from reana_db.database import Session
    from reana_db.models import ResourceType, WorkflowResource

    def _get_disk_usage_or_zero(workflow):
        """Get disk usage for a workflow if the workspace exists, zero if not."""
        try:
            disk_bytes = get_disk_usage(workflow.workspace_path, summarize=True)
            return int(disk_bytes[0]["size"]["raw"])
        except REANAMissingWorkspaceError:
            return 0

    disk_resource = get_default_quota_resource(ResourceType.disk.name)
    workflow_resource = (
        Session.query(WorkflowResource)
        .filter_by(workflow_id=workflow.id_, resource_id=disk_resource.id_)
        .one_or_none()
    )

    if workflow_resource:
        if bytes_to_sum:
            workflow_resource.quota_used += bytes_to_sum
        else:
            workflow_resource.quota_used = _get_disk_usage_or_zero(workflow)
        Session.commit()
    elif inspect(workflow).persistent:
        workflow_resource = WorkflowResource(
            workflow_id=workflow.id_,
            resource_id=disk_resource.id_,
            quota_used=_get_disk_usage_or_zero(workflow),
        )
        Session.add(workflow_resource)
        Session.commit()

    return workflow_resource
