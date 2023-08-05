/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

#pragma once

#include "tls/extensions/s2n_extension_type.h"
#include "tls/s2n_connection.h"
#include "stuffer/s2n_stuffer.h"

extern const s2n_extension_type s2n_server_session_ticket_extension;

/* Old-style extension functions -- remove after extensions refactor is complete */
int s2n_recv_server_session_ticket_ext(struct s2n_connection *conn, struct s2n_stuffer *extension);
int s2n_send_server_session_ticket_ext(struct s2n_connection *conn, struct s2n_stuffer *out);
int s2n_server_session_ticket_ext_size(struct s2n_connection *conn);
