# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import render_template, Response

from app import init_connection_pool, update_account


def main(request):
    db = init_connection_pool()
    body = request.get_json()
    update_account(db, account_id=body["account_id"], balance=body["balance"], user_id=body["user_id"])
    return Response(
        response="Account updated.",
        status=200,
    )
