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

#include "tls/extensions/s2n_client_supported_groups.h"
#include "tls/extensions/s2n_ec_point_format.h"

#include "tls/s2n_tls.h"
#include "tls/s2n_tls_parameters.h"
#include "tls/s2n_security_policies.h"

#include "utils/s2n_safety.h"
#include "crypto/s2n_fips.h"
#include "tls/s2n_tls13.h"

static int s2n_client_supported_groups_send(struct s2n_connection *conn, struct s2n_stuffer *out);
static int s2n_client_supported_groups_recv(struct s2n_connection *conn, struct s2n_stuffer *extension);

const s2n_extension_type s2n_client_supported_groups_extension = {
    .iana_value = TLS_EXTENSION_SUPPORTED_GROUPS,
    .is_response = false,
    .send = s2n_client_supported_groups_send,
    .recv = s2n_client_supported_groups_recv,
    .should_send = s2n_extension_should_send_if_ecc_enabled,
    .if_missing = s2n_extension_noop_if_missing,
};

bool s2n_extension_should_send_if_ecc_enabled(struct s2n_connection *conn)
{
    const struct s2n_security_policy *security_policy;
    return s2n_connection_get_security_policy(conn, &security_policy) == S2N_SUCCESS
            && s2n_ecc_is_extension_required(security_policy);
}

static int s2n_client_supported_groups_send(struct s2n_connection *conn, struct s2n_stuffer *out)
{
    notnull_check(conn);

    const struct s2n_ecc_preferences *ecc_pref = NULL;
    GUARD(s2n_connection_get_ecc_preferences(conn, &ecc_pref));
    notnull_check(ecc_pref);

    const struct s2n_kem_preferences *kem_pref = NULL;
    GUARD(s2n_connection_get_kem_preferences(conn, &kem_pref));
    notnull_check(kem_pref);

    /* Group list len */
    struct s2n_stuffer_reservation group_list_len = { 0 };
    GUARD(s2n_stuffer_reserve_uint16(out, &group_list_len));

    /* Send KEM groups list first */
    if (s2n_is_tls13_enabled() && !s2n_is_in_fips_mode()) {
        for (size_t i = 0; i < kem_pref->tls13_kem_group_count; i++) {
            GUARD(s2n_stuffer_write_uint16(out, kem_pref->tls13_kem_groups[i]->iana_id));
        }
    }

    /* Then send curve list */
    for (size_t i = 0; i < ecc_pref->count; i++) {
        GUARD(s2n_stuffer_write_uint16(out, ecc_pref->ecc_curves[i]->iana_id));
    }

    GUARD(s2n_stuffer_write_vector_size(&group_list_len));

    return S2N_SUCCESS;
}

/* Populates the appropriate index of either the mutually_supported_curves or
 * mutually_supported_kem_groups array based on the received IANA ID. Will
 * ignore unrecognized IANA IDs (and return success). */
static int s2n_client_supported_groups_recv_iana_id(struct s2n_connection *conn, uint16_t iana_id) {
    notnull_check(conn);

    const struct s2n_ecc_preferences *ecc_pref = NULL;
    GUARD(s2n_connection_get_ecc_preferences(conn, &ecc_pref));
    notnull_check(ecc_pref);

    for (size_t i = 0; i < ecc_pref->count; i++) {
        const struct s2n_ecc_named_curve *supported_curve = ecc_pref->ecc_curves[i];
        if (iana_id == supported_curve->iana_id) {
            conn->secure.mutually_supported_curves[i] = supported_curve;
            return S2N_SUCCESS;
        }
    }

    /* Return early if in FIPS mode, or if TLS 1.3 is disabled, so as to ignore PQ IDs */
    if (s2n_is_in_fips_mode() || !s2n_is_tls13_enabled()) {
        return S2N_SUCCESS;
    }

    const struct s2n_kem_preferences *kem_pref = NULL;
    GUARD(s2n_connection_get_kem_preferences(conn, &kem_pref));
    notnull_check(kem_pref);

    for (size_t i = 0; i < kem_pref->tls13_kem_group_count; i++) {
        const struct s2n_kem_group *supported_kem_group = kem_pref->tls13_kem_groups[i];
        if (iana_id == supported_kem_group->iana_id) {
            conn->secure.mutually_supported_kem_groups[i] = supported_kem_group;
            return S2N_SUCCESS;
        }
    }

    return S2N_SUCCESS;
}

static int s2n_choose_supported_group(struct s2n_connection *conn) {
    notnull_check(conn);

    const struct s2n_ecc_preferences *ecc_pref = NULL;
    GUARD(s2n_connection_get_ecc_preferences(conn, &ecc_pref));
    notnull_check(ecc_pref);

    const struct s2n_kem_preferences *kem_pref = NULL;
    GUARD(s2n_connection_get_kem_preferences(conn, &kem_pref));
    notnull_check(kem_pref);

    /* Ensure that only the intended group will be non-NULL (if no group is chosen, everything
     * should be NULL). */
    conn->secure.server_kem_group_params.kem_group = NULL;
    conn->secure.server_kem_group_params.ecc_params.negotiated_curve = NULL;
    conn->secure.server_kem_group_params.kem_params.kem = NULL;
    conn->secure.server_ecc_evp_params.negotiated_curve = NULL;

    /* Prefer to negotiate hybrid PQ over ECC. If in FIPS mode, we will never choose a
     * PQ group because the mutually_supported_kem_groups array will not have been
     * populated with anything. */
    for (size_t i = 0; i < kem_pref->tls13_kem_group_count; i++) {
        const struct s2n_kem_group *candidate_kem_group = conn->secure.mutually_supported_kem_groups[i];
        if (candidate_kem_group != NULL) {
            conn->secure.server_kem_group_params.kem_group = candidate_kem_group;
            conn->secure.server_kem_group_params.ecc_params.negotiated_curve = candidate_kem_group->curve;
            conn->secure.server_kem_group_params.kem_params.kem = candidate_kem_group->kem;
            return S2N_SUCCESS;
        }
    }

    for (size_t i = 0; i < ecc_pref->count; i++) {
        const struct s2n_ecc_named_curve *candidate_curve = conn->secure.mutually_supported_curves[i];
        if (candidate_curve != NULL) {
            conn->secure.server_ecc_evp_params.negotiated_curve = candidate_curve;
            return S2N_SUCCESS;
        }
    }

    return S2N_SUCCESS;
}

static int s2n_client_supported_groups_recv(struct s2n_connection *conn, struct s2n_stuffer *extension) {
    notnull_check(conn);
    notnull_check(extension);

    uint16_t size_of_all;
    GUARD(s2n_stuffer_read_uint16(extension, &size_of_all));
    if (size_of_all > s2n_stuffer_data_available(extension) || (size_of_all % sizeof(uint16_t))) {
        /* Malformed length, ignore the extension */
        return S2N_SUCCESS;
    }

    for (size_t i = 0; i < (size_of_all / sizeof(uint16_t)); i++) {
        uint16_t iana_id;
        GUARD(s2n_stuffer_read_uint16(extension, &iana_id));
        GUARD(s2n_client_supported_groups_recv_iana_id(conn, iana_id));
    }

    GUARD(s2n_choose_supported_group(conn));

    return S2N_SUCCESS;
}

/* Old-style extension functions -- remove after extensions refactor is complete */

int s2n_extensions_client_supported_groups_send(struct s2n_connection *conn, struct s2n_stuffer *out)
{
    GUARD(s2n_extension_send(&s2n_client_supported_groups_extension, conn, out));

    /* The original send method also sent ec point formats. To avoid breaking
     * anything, I'm going to let it continue writing point formats.
     */
    GUARD(s2n_extension_send(&s2n_client_ec_point_format_extension, conn, out));

    return S2N_SUCCESS;
}

int s2n_recv_client_supported_groups(struct s2n_connection *conn, struct s2n_stuffer *extension)
{
    return s2n_extension_recv(&s2n_client_supported_groups_extension, conn, extension);
}
