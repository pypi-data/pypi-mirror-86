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

#include <sys/param.h>
#include <stdint.h>

#include "tls/extensions/s2n_client_max_frag_len.h"
#include "tls/s2n_tls.h"
#include "tls/s2n_tls_parameters.h"

#include "utils/s2n_safety.h"

static bool s2n_client_max_frag_len_should_send(struct s2n_connection *conn);
static int s2n_client_max_frag_len_send(struct s2n_connection *conn, struct s2n_stuffer *out);
static int s2n_client_max_frag_len_recv(struct s2n_connection *conn, struct s2n_stuffer *extension);

const s2n_extension_type s2n_client_max_frag_len_extension = {
    .iana_value = TLS_EXTENSION_MAX_FRAG_LEN,
    .is_response = false,
    .send = s2n_client_max_frag_len_send,
    .recv = s2n_client_max_frag_len_recv,
    .should_send = s2n_client_max_frag_len_should_send,
    .if_missing = s2n_extension_noop_if_missing,
};

static bool s2n_client_max_frag_len_should_send(struct s2n_connection *conn)
{
    return conn->config->mfl_code != S2N_TLS_MAX_FRAG_LEN_EXT_NONE;
}

static int s2n_client_max_frag_len_send(struct s2n_connection *conn, struct s2n_stuffer *out)
{
    return s2n_stuffer_write_uint8(out, conn->config->mfl_code);
}

static int s2n_client_max_frag_len_recv(struct s2n_connection *conn, struct s2n_stuffer *extension)
{
    if (!conn->config->accept_mfl) {
        return S2N_SUCCESS;
    }

    uint8_t mfl_code;
    GUARD(s2n_stuffer_read_uint8(extension, &mfl_code));
    if (mfl_code > S2N_TLS_MAX_FRAG_LEN_4096 || mfl_code_to_length[mfl_code] > S2N_TLS_MAXIMUM_FRAGMENT_LENGTH) {
        return S2N_SUCCESS;
    }

    conn->mfl_code = mfl_code;
    conn->max_outgoing_fragment_length = mfl_code_to_length[mfl_code];
    return S2N_SUCCESS;
}

/* Old-style extension functions -- remove after extensions refactor is complete */

int s2n_extensions_client_max_frag_len_send(struct s2n_connection *conn, struct s2n_stuffer *out)
{
    return s2n_extension_send(&s2n_client_max_frag_len_extension, conn, out);
}

int s2n_recv_client_max_frag_len(struct s2n_connection *conn, struct s2n_stuffer *extension)
{
    return s2n_extension_recv(&s2n_client_max_frag_len_extension, conn, extension);
}
