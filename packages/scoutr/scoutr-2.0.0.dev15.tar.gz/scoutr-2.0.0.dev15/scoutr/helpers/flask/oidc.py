import os
from typing import List

from flask_api.request import APIRequest

from scoutr.exceptions import UnauthorizedException
from scoutr.models.request import Request, UserData, RequestUser
from scoutr.providers.base.api import BaseAPI


def get_user_from_oidc(api: BaseAPI, request: APIRequest) -> RequestUser:
    groups: List[str] = []

    # Return a dummy user when in debug mode
    if os.getenv('DEBUG', 'false') == 'true':
        group_string = os.getenv('GROUPS', '')
        if group_string:
            groups = group_string.split(',')

        return RequestUser(
            id='222222222',
            data=UserData(
                username='222222222',
                email='george.p.burdell@ge.com',
                name='Georgia Burdell',
                groups=groups
            )
        )

    if api.config.oidc_group_header:
        group_string = request.headers.get(api.config.oidc_group_header, '')
        if group_string == '':
            groups = []
        else:
            groups = group_string.split(',')

    # Permit tuples for the name header in case the name is split into first and last name
    if isinstance(api.config.oidc_name_header, tuple):
        name_parts = []
        for header in api.config.oidc_name_header:
            value = request.headers.get(header)
            if header:
                name_parts.append(value)
        name = ' '.join([
            request.headers.get(header)
            for header in api.config.oidc_name_header
            if request.headers.get(header)
        ]) or None
    else:
        name = request.headers.get(api.config.oidc_name_header)

    username = request.headers.get(api.config.oidc_username_header)
    if not username:
        raise UnauthorizedException('Unable to determine user id')

    user_data = UserData(
        name=name,
        email=request.headers.get(api.config.oidc_username_header),
        username=request.headers.get(api.config.oidc_username_header),
        groups=groups
    )

    return RequestUser(
        id=user_data.username,
        data=user_data
    )


def build_oidc_request(api: BaseAPI, request: APIRequest) -> Request:
    from scoutr.helpers.flask.utils import parse_query_params

    req = Request(
        method=request.method,
        path=request.path,
        source_ip=request.remote_addr,
        user_agent=request.user_agent.string,
        user=get_user_from_oidc(api, request)
    )

    query_params = parse_query_params(request.query_string)
    if query_params:
        req.query_params = query_params

    if request.data:
        req.body = request.data

    return req
