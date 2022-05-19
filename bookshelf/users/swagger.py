from drf_yasg import openapi

put_profile = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[],
    properties={
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            title="first_name",
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            title="last_name",
        ),
        'birth_date': openapi.Schema(
            type=openapi.FORMAT_DATE,
            title="birth_date",
        ),
        'info': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="info",
        ),
    },
    example={
        'first_name': 'Samuel',
        'last_name': 'Jackson',
        'birth_date': '2021-04-18',
        'info': {
                "interestings": ['come to school']
            },
    }
)

patch_profile = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[],
    properties={
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            title="first_name",
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            title="last_name",
        ),
        'birth_date': openapi.Schema(
            type=openapi.FORMAT_DATE,
            title="birth_date",
        ),
        'info': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="info",
        ),
    },
    example={
        'first_name': 'Samuel',
        'last_name': None,
        'birth_date': None,
        'info': {
                "interestings": ['come to school']
            },
    }
)

username_param = openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING)