from contextlib import nullcontext as does_not_raise

PARAMS_TEST_CHECK_ACCOUNT_ROUTER = [
    (
        'api/v1/auth/check_account/ivan.ivanov@example.com',
        {}, {}, 200, {
            'message': 'Код подтверждения отправлен на ваш e-mail',
            'account': 'ivan.ivanov@example.com',
        }, does_not_raise(),
    ),
]

PARAMS_TEST_SIGN_UP_ROUTER = [
    (
        'api/v1/auth/sign-up',
        {
            'account': 'ivan.ivanov@example.com',
            'token': '1234'
        },
        {}, 200, {}, does_not_raise(),
    ),
]