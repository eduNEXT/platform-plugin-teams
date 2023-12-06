"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "platform_plugin_teams",
)

LOCALE_PATHS = [
    root("platform_plugin_teams", "conf", "locale"),
]

ROOT_URLCONF = "platform_plugin_teams.urls"

SECRET_KEY = "insecure-secret-key"

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",  # this is required for admin
                "django.contrib.messages.context_processors.messages",  # this is required for admin
            ],
        },
    }
]

SERVICE_VARIANT = "lms"


PLATFORM_PLUGIN_TEAMS_STUDENT_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.student_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_TEAMS_COMMON_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.teams_common_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_TEAMS_LMS_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.teams_lms_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_COURSEWARE_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.courseware_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_MODULESTORE_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.modulestore_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_AUTHENTICATION_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.authentication_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_TEAMS_CONFIG_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.teams_config_p_v1_test"
)
PLATFORM_PLUGIN_TEAMS_CONTENTSTORE_BACKEND = (
    "platform_plugin_teams.edxapp_wrapper.backends.contentstore_p_v1_test"
)
