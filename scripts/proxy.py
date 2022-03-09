#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ahapi
import typing

"""Proxy assignment end point for ASFMM"""


async def process(state: typing.Any, request, formdata: dict) -> typing.Any:
    cookie = state.cookies.get(request)  # Fetches a valid session or None if not found
    if not cookie or not cookie.state or not cookie.state.get("credentials"):
        return {"success": False, "message": "Oops, something went terribly wrong here!"}

    whoami = cookie.state["credentials"]["login"]
    if whoami.startswith("guest_"):
        return {"success": False, "message": "Guests cannot assign proxies"}

    assigned = 0
    invalid = 0
    for member in formdata.get("members"):
        if member and member in state.members:
            state.quorum.add(member)
            assigned += 1
        elif member:
            invalid += 1
    if not invalid:
        return {
            "success": True,
            "message": f"{assigned} proxies assigned to you."
        }
    else:
        return {
            "success": True,
            "message": f"{assigned} proxies assigned to you. {invalid} proxies were invalid or already assigned."
        }


def register(state: typing.Any):
    return ahapi.endpoint(process)
