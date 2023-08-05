/**
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0.
 */
#include "module.h"

#include "auth.h"
#include "crypto.h"
#include "event_stream.h"
#include "http.h"
#include "io.h"
#include "mqtt_client.h"
#include "mqtt_client_connection.h"

#include <aws/auth/auth.h>
#include <aws/common/byte_buf.h>
#include <aws/common/system_info.h>
#include <aws/event-stream/event_stream.h>
#include <aws/http/http.h>
#include <aws/io/io.h>
#include <aws/io/logging.h>
#include <aws/io/tls_channel_handler.h>
#include <aws/mqtt/mqtt.h>

#include <memoryobject.h>

static struct aws_logger s_logger;
static bool s_logger_init = false;

PyObject *aws_py_init_logging(PyObject *self, PyObject *args) {
    (void)self;

    if (s_logger_init) {
        aws_logger_set(NULL);
        aws_logger_clean_up(&s_logger);
    }

    s_logger_init = true;

    struct aws_allocator *allocator = aws_py_get_allocator();

    int log_level = 0;
    const char *file_path = NULL;
    Py_ssize_t file_path_len = 0;

    if (!PyArg_ParseTuple(args, "bs#", &log_level, &file_path, &file_path_len)) {
        PyErr_SetNone(PyExc_ValueError);
        return NULL;
    }

    struct aws_logger_standard_options log_options = {
        .level = log_level,
        .file = NULL,
        .filename = NULL,
    };

    Py_ssize_t stdout_len = (Py_ssize_t)strlen("stdout");

    Py_ssize_t cmp_len = file_path_len > stdout_len ? stdout_len : file_path_len;

    if (!memcmp("stdout", file_path, (size_t)cmp_len)) {
        log_options.file = stdout;
    } else if (!memcmp("stderr", file_path, (size_t)cmp_len)) {
        log_options.file = stderr;
    } else {
        log_options.filename = file_path;
    }

    aws_logger_init_standard(&s_logger, allocator, &log_options);
    aws_logger_set(&s_logger);

    Py_RETURN_NONE;
}

struct aws_byte_cursor aws_byte_cursor_from_pyunicode(PyObject *str) {
    Py_ssize_t len;
    const char *ptr = PyUnicode_AsUTF8AndSize(str, &len);
    if (ptr) {
        return aws_byte_cursor_from_array(ptr, (size_t)len);
    }
    return aws_byte_cursor_from_array(NULL, 0);
}

struct aws_byte_cursor aws_byte_cursor_from_pybytes(PyObject *py_bytes) {
    char *ptr;
    Py_ssize_t len;
    if (PyBytes_AsStringAndSize(py_bytes, &ptr, &len) == -1) {
        return aws_byte_cursor_from_array(NULL, 0);
    }

    return aws_byte_cursor_from_array(ptr, (size_t)len);
}

PyObject *PyUnicode_FromAwsByteCursor(const struct aws_byte_cursor *cursor) {
    if (cursor->len > PY_SSIZE_T_MAX) {
        PyErr_SetString(PyExc_OverflowError, "Cursor exceeds PY_SSIZE_T_MAX");
        return NULL;
    }
    return PyUnicode_FromStringAndSize((const char *)cursor->ptr, (Py_ssize_t)cursor->len);
}

PyObject *PyUnicode_FromAwsString(const struct aws_string *aws_str) {
    if (aws_str->len > PY_SSIZE_T_MAX) {
        PyErr_SetString(PyExc_OverflowError, "String exceeds PY_SSIZE_T_MAX");
        return NULL;
    }
    return PyUnicode_FromStringAndSize(aws_string_c_str(aws_str), aws_str->len);
}

uint32_t PyObject_GetAttrAsUint32(PyObject *o, const char *class_name, const char *attr_name) {
    uint32_t result = UINT32_MAX;

    PyObject *attr = PyObject_GetAttrString(o, attr_name);
    if (!attr) {
        PyErr_Format(PyExc_AttributeError, "'%s.%s' attribute not found", class_name, attr_name);
        return result;
    }

    /* Using PyLong_AsLongLong() because it will convert floating point numbers (PyLong_AsUnsignedLong() will not).
     * By using "long long" (not just "long") we can be sure to fit the whole range of 32bit numbers. */
    long long val = PyLong_AsLongLong(attr);
    if (PyErr_Occurred()) {
        PyErr_Format(PyErr_Occurred(), "Cannot convert %s.%s to a C uint32_t", class_name, attr_name);
        goto done;
    }

    if (val < 0) {
        PyErr_Format(PyExc_OverflowError, "%s.%s cannot be negative", class_name, attr_name);
        goto done;
    }

    if (val > UINT32_MAX) {
        PyErr_Format(PyExc_OverflowError, "%s.%s too large to convert to C uint32_t", class_name, attr_name);
        goto done;
    }

    result = (uint32_t)val;
done:
    Py_DECREF(attr);
    return result;
}

uint16_t PyObject_GetAttrAsUint16(PyObject *o, const char *class_name, const char *attr_name) {
    uint16_t result = UINT16_MAX;

    PyObject *attr = PyObject_GetAttrString(o, attr_name);
    if (!attr) {
        PyErr_Format(PyExc_AttributeError, "'%s.%s' attribute not found", class_name, attr_name);
        return result;
    }

    /* Using PyLong_AsLong() because it will convert floating point numbers (PyLong_AsUnsignedLong() will not) */
    long val = PyLong_AsLong(attr);
    if (PyErr_Occurred()) {
        PyErr_Format(PyErr_Occurred(), "Cannot convert %s.%s to C uint16_t", class_name, attr_name);
        goto done;
    }

    if (val < 0) {
        PyErr_Format(PyExc_OverflowError, "%s.%s cannot be negative", class_name, attr_name);
        goto done;
    }

    if (val > UINT16_MAX) {
        PyErr_Format(PyExc_OverflowError, "%s.%s too large to convert to C uint16_t", class_name, attr_name);
        goto done;
    }

    result = (uint16_t)val;
done:
    Py_DECREF(attr);
    return result;
}

bool PyObject_GetAttrAsBool(PyObject *o, const char *class_name, const char *attr_name) {
    bool result = false;

    PyObject *attr = PyObject_GetAttrString(o, attr_name);
    if (!attr) {
        PyErr_Format(PyExc_AttributeError, "'%s.%s' attribute not found", class_name, attr_name);
        return result;
    }

    int val = PyObject_IsTrue(attr);
    if (val == -1) {
        PyErr_Format(PyExc_TypeError, "Cannot convert %s.%s to bool", class_name, attr_name);
        goto done;
    }

    result = val != 0;
done:
    Py_DECREF(attr);
    return result;
}

int PyObject_GetAttrAsIntEnum(PyObject *o, const char *class_name, const char *attr_name) {
    int result = -1;

    PyObject *attr = PyObject_GetAttrString(o, attr_name);
    if (!attr) {
        PyErr_Format(PyExc_AttributeError, "'%s.%s' attribute not found", class_name, attr_name);
        return result;
    }

    if (!PyLong_Check(attr)) {
        PyErr_Format(PyExc_TypeError, "%s.%s is not a valid enum", class_name, attr_name);
        goto done;
    }

    result = PyLong_AsLong(attr);
done:
    Py_DECREF(attr);
    return result;
}

void PyErr_SetAwsLastError(void) {
    PyErr_AwsLastError();
}

PyObject *PyErr_AwsLastError(void) {
    int err = aws_last_error();
    const char *name = aws_error_name(err);
    const char *msg = aws_error_str(err);
    return PyErr_Format(PyExc_RuntimeError, "%d (%s): %s", err, name, msg);
}

/* Mappings between Python built-in exception types and AWS_ERROR_ codes
 * Stored in hashtables as `PyObject*` of Python exception type, and `int` of AWS_ERROR_ enum (cast to void*) */
static struct aws_hash_table s_py_to_aws_error_map;
static struct aws_hash_table s_aws_to_py_error_map;

static void s_error_map_init(void) {
    struct error_pair {
        PyObject *py_exception_type;
        int aws_error_code;
    };

    /* If the same key is listed multiple times, later entries overwrite earlier entries
     * Ex: Both TypeError and ValueError map to INVALID_ARG, but INVALID_ARG only maps to ValueError. */
    struct error_pair s_error_array[] = {
        {PyExc_IndexError, AWS_ERROR_INVALID_INDEX},
        {PyExc_MemoryError, AWS_ERROR_OOM},
        {PyExc_NotImplementedError, AWS_ERROR_UNIMPLEMENTED},
        {PyExc_OverflowError, AWS_ERROR_OVERFLOW_DETECTED},
        {PyExc_TypeError, AWS_ERROR_INVALID_ARGUMENT},
        {PyExc_ValueError, AWS_ERROR_INVALID_ARGUMENT},
        {PyExc_FileNotFoundError, AWS_ERROR_FILE_INVALID_PATH},
        {PyExc_BlockingIOError, AWS_IO_READ_WOULD_BLOCK},
        {PyExc_BrokenPipeError, AWS_IO_BROKEN_PIPE},
    };

    if (aws_hash_table_init(
            &s_py_to_aws_error_map,
            aws_py_get_allocator(),
            AWS_ARRAY_SIZE(s_error_array),
            aws_hash_ptr,
            aws_ptr_eq,
            NULL /*destroy_key_fn*/,
            NULL /*destroy_value_fn*/)) {
        AWS_FATAL_ASSERT(0);
    }

    if (aws_hash_table_init(
            &s_aws_to_py_error_map,
            aws_py_get_allocator(),
            AWS_ARRAY_SIZE(s_error_array),
            aws_hash_ptr,
            aws_ptr_eq,
            NULL /*destroy_key_fn*/,
            NULL /*destroy_value_fn*/)) {
        AWS_FATAL_ASSERT(0);
    }

    for (size_t i = 0; i < AWS_ARRAY_SIZE(s_error_array); ++i) {
        void *py_exc = s_error_array[i].py_exception_type;
        void *aws_err = (void *)(size_t)s_error_array[i].aws_error_code;
        if (aws_hash_table_put(&s_py_to_aws_error_map, py_exc, aws_err, NULL)) {
            AWS_FATAL_ASSERT(0);
        }
        if (aws_hash_table_put(&s_aws_to_py_error_map, aws_err, py_exc, NULL)) {
            AWS_FATAL_ASSERT(0);
        }
    }
}

int aws_py_raise_error(void) {
    AWS_ASSERT(PyErr_Occurred() != NULL);
    AWS_ASSERT(PyGILState_Check() == 1);

    int aws_error_code = AWS_ERROR_UNKNOWN;

    struct aws_hash_element *found;
    aws_hash_table_find(&s_py_to_aws_error_map, PyErr_Occurred(), &found);
    if (found) {
        aws_error_code = (int)(size_t)found->value;
    }

    /* Print standard traceback to sys.stderr and clear the error indicator. */
    PyErr_Print();
    fprintf(stderr, "Treating Python exception as error %d(%s)\n", aws_error_code, aws_error_name(aws_error_code));

    return aws_raise_error(aws_error_code);
}

PyObject *aws_py_get_corresponding_builtin_exception(PyObject *self, PyObject *args) {
    (void)self;
    int error_code;
    if (!PyArg_ParseTuple(args, "i", &error_code)) {
        return NULL;
    }

    struct aws_hash_element *found;
    aws_hash_table_find(&s_aws_to_py_error_map, (void *)(size_t)error_code, &found);
    if (!found) {
        Py_RETURN_NONE;
    }

    PyObject *py_exception_type = found->value;
    Py_INCREF(py_exception_type);
    return py_exception_type;
}

PyObject *aws_py_get_error_name(PyObject *self, PyObject *args) {
    (void)self;
    int error_code;
    if (!PyArg_ParseTuple(args, "i", &error_code)) {
        return NULL;
    }

    const char *name = aws_error_name(error_code);
    return PyUnicode_FromString(name);
}

PyObject *aws_py_get_error_message(PyObject *self, PyObject *args) {
    (void)self;
    int error_code;
    if (!PyArg_ParseTuple(args, "i", &error_code)) {
        return NULL;
    }

    const char *name = aws_error_str(error_code);
    return PyUnicode_FromString(name);
}

PyObject *aws_py_memory_view_from_byte_buffer(struct aws_byte_buf *buf) {
    size_t available = buf->capacity - buf->len;
    if (available > PY_SSIZE_T_MAX) {
        PyErr_SetString(PyExc_OverflowError, "Buffer exceeds PY_SSIZE_T_MAX");
        return NULL;
    }

    Py_ssize_t mem_size = available;
    char *mem_start = (char *)(buf->buffer + buf->len);
    return PyMemoryView_FromMemory(mem_start, mem_size, PyBUF_WRITE);
}

int aws_py_gilstate_ensure(PyGILState_STATE *out_state) {
    if (AWS_LIKELY(Py_IsInitialized())) {
        *out_state = PyGILState_Ensure();
        return AWS_OP_SUCCESS;
    }

    return aws_raise_error(AWS_ERROR_INVALID_STATE);
}

void *aws_py_get_binding(PyObject *obj, const char *capsule_name, const char *class_name) {
    if (!obj || obj == Py_None) {
        return PyErr_Format(PyExc_TypeError, "Excepted '%s', received 'NoneType'", class_name);
    }

    PyObject *py_binding = PyObject_GetAttrString(obj, "_binding"); /* new reference */
    if (!py_binding) {
        return PyErr_Format(
            PyExc_AttributeError,
            "Expected valid '%s', received '%s' (no '_binding' attribute)",
            class_name,
            Py_TYPE(obj)->tp_name);
    }

    void *binding = NULL;
    if (!PyCapsule_CheckExact(py_binding)) {
        PyErr_Format(
            PyExc_TypeError,
            "Expected valid '%s', received '%s' ('_binding' attribute is not a capsule)",
            class_name,
            Py_TYPE(obj)->tp_name);
        goto done;
    }

    binding = PyCapsule_GetPointer(py_binding, capsule_name);
    if (!binding) {
        PyErr_Format(
            PyExc_TypeError,
            "Expected valid '%s', received '%s' ('_binding' attribute does not contain '%s')",
            class_name,
            Py_TYPE(obj)->tp_name,
            capsule_name);
        goto done;
    }

done:
    Py_DECREF(py_binding);
    return binding;
}

/*******************************************************************************
 * Allocator
 ******************************************************************************/

struct aws_allocator *aws_py_get_allocator(void) {
    return aws_default_allocator();
}

/*******************************************************************************
 * Crash handler
 ******************************************************************************/
#if defined(_WIN32)
#    include <windows.h>
static LONG WINAPI s_print_stack_trace(struct _EXCEPTION_POINTERS *exception_pointers) {
    aws_backtrace_print(stderr, exception_pointers);
    return EXCEPTION_EXECUTE_HANDLER;
}
#elif defined(AWS_HAVE_EXECINFO)
#    include <signal.h>
static void s_print_stack_trace(int sig, siginfo_t *sig_info, void *user_data) {
    (void)sig;
    (void)sig_info;
    (void)user_data;
    aws_backtrace_print(stderr, sig_info);
    exit(-1);
}
#endif

static void s_install_crash_handler(void) {
#if defined(_WIN32)
    SetUnhandledExceptionFilter(s_print_stack_trace);
#elif defined(AWS_HAVE_EXECINFO)
    struct sigaction sa;
    memset(&sa, 0, sizeof(struct sigaction));
    sigemptyset(&sa.sa_mask);

    sa.sa_flags = SA_NODEFER;
    sa.sa_sigaction = s_print_stack_trace;

    sigaction(SIGSEGV, &sa, NULL);
    sigaction(SIGABRT, &sa, NULL);
    sigaction(SIGILL, &sa, NULL);
    sigaction(SIGBUS, &sa, NULL);
#endif
}

/*******************************************************************************
 * Definitions
 ******************************************************************************/

#define AWS_PY_METHOD_DEF(NAME, FLAGS)                                                                                 \
    { #NAME, aws_py_##NAME, (FLAGS), NULL }

static PyMethodDef s_module_methods[] = {
    /* Common */
    AWS_PY_METHOD_DEF(get_error_name, METH_VARARGS),
    AWS_PY_METHOD_DEF(get_error_message, METH_VARARGS),
    AWS_PY_METHOD_DEF(get_corresponding_builtin_exception, METH_VARARGS),

    /* IO */
    AWS_PY_METHOD_DEF(is_alpn_available, METH_NOARGS),
    AWS_PY_METHOD_DEF(event_loop_group_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(host_resolver_new_default, METH_VARARGS),
    AWS_PY_METHOD_DEF(client_bootstrap_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(client_tls_ctx_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(tls_connections_options_new_from_ctx, METH_VARARGS),
    AWS_PY_METHOD_DEF(tls_connection_options_set_alpn_list, METH_VARARGS),
    AWS_PY_METHOD_DEF(tls_connection_options_set_server_name, METH_VARARGS),
    AWS_PY_METHOD_DEF(init_logging, METH_VARARGS),
    AWS_PY_METHOD_DEF(input_stream_new, METH_VARARGS),

    /* MQTT Client */
    AWS_PY_METHOD_DEF(mqtt_client_new, METH_VARARGS),

    /* MQTT Client Connection */
    AWS_PY_METHOD_DEF(mqtt_client_connection_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_connect, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_reconnect, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_publish, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_subscribe, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_on_message, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_resubscribe_existing_topics, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_unsubscribe, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_client_connection_disconnect, METH_VARARGS),
    AWS_PY_METHOD_DEF(mqtt_ws_handshake_transform_complete, METH_VARARGS),

    /* Cryptographic primitives */
    AWS_PY_METHOD_DEF(md5_new, METH_NOARGS),
    AWS_PY_METHOD_DEF(sha256_new, METH_NOARGS),
    AWS_PY_METHOD_DEF(hash_update, METH_VARARGS),
    AWS_PY_METHOD_DEF(hash_digest, METH_VARARGS),
    AWS_PY_METHOD_DEF(sha256_hmac_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(hash_update, METH_VARARGS),
    AWS_PY_METHOD_DEF(hash_digest, METH_VARARGS),

    /* HTTP */
    AWS_PY_METHOD_DEF(http_connection_close, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_connection_is_open, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_client_connection_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_client_stream_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_client_stream_activate, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_new_request, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_get_request_method, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_set_request_method, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_get_request_path, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_set_request_path, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_get_body_stream, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_message_set_body_stream, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_add, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_add_pairs, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_set, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_get, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_get_index, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_count, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_remove, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_remove_value, METH_VARARGS),
    AWS_PY_METHOD_DEF(http_headers_clear, METH_VARARGS),

    /* Auth */
    AWS_PY_METHOD_DEF(credentials_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(credentials_access_key_id, METH_VARARGS),
    AWS_PY_METHOD_DEF(credentials_secret_access_key, METH_VARARGS),
    AWS_PY_METHOD_DEF(credentials_session_token, METH_VARARGS),
    AWS_PY_METHOD_DEF(credentials_provider_get_credentials, METH_VARARGS),
    AWS_PY_METHOD_DEF(credentials_provider_new_chain_default, METH_VARARGS),
    AWS_PY_METHOD_DEF(credentials_provider_new_static, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_new, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_algorithm, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_signature_type, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_credentials_provider, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_region, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_service, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_date, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_use_double_uri_encode, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_should_normalize_uri_path, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_signed_body_value, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_signed_body_header_type, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_expiration_in_seconds, METH_VARARGS),
    AWS_PY_METHOD_DEF(signing_config_get_omit_session_token, METH_VARARGS),
    AWS_PY_METHOD_DEF(sign_request_aws, METH_VARARGS),

    /* Event Stream */
    AWS_PY_METHOD_DEF(event_stream_rpc_client_connection_connect, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_connection_close, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_connection_is_open, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_connection_send_protocol_message, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_connection_new_stream, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_continuation_activate, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_continuation_send_message, METH_VARARGS),
    AWS_PY_METHOD_DEF(event_stream_rpc_client_continuation_is_closed, METH_VARARGS),

    {NULL, NULL, 0, NULL},
};

static const char s_module_name[] = "_awscrt";
PyDoc_STRVAR(s_module_doc, "C extension for binding AWS implementations of MQTT, HTTP, and friends");

/*******************************************************************************
 * Module Init
 ******************************************************************************/

PyMODINIT_FUNC PyInit__awscrt(void) {
    static struct PyModuleDef s_module_def = {
        PyModuleDef_HEAD_INIT,
        s_module_name,
        s_module_doc,
        -1, /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
        s_module_methods,
        NULL, /* slots for multi-phase initialization */
        NULL, /* traversal fn to call during GC traversal */
        NULL, /* clear fn to call during GC clear */
        NULL, /* fn to call during deallocation of the module object */
    };

    PyObject *m = PyModule_Create(&s_module_def);
    if (!m) {
        return NULL;
    }

    s_install_crash_handler();

    aws_http_library_init(aws_py_get_allocator());
    aws_auth_library_init(aws_py_get_allocator());
    aws_mqtt_library_init(aws_py_get_allocator());
    aws_event_stream_library_init(aws_py_get_allocator());

#if PY_MAJOR_VERSION == 3 && PY_MINOR_VERSION < 9
    if (!PyEval_ThreadsInitialized()) {
        PyEval_InitThreads();
    }
#endif

    s_error_map_init();

    return m;
}
