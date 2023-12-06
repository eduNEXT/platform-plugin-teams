Platform Plugin Teams
#####################

|ci-badge| |license-badge| |status-badge|


Purpose
*******

Open edX plugin that includes a custom teams API, which extends the
functionality of the Open edX teams API. Compared to the existing teams
API, this plugin includes new views to create and delete a topic and extends
listing topics to include the list of teams within each topic. It also extends
the functionality of adding a user to a team so multiple users can be added to
a team by using a list of usernames.

This plugin has been created as an open source contribution to the Open edX
platform and has been funded by the Unidigital project from the Spanish
Government - 2023.


Getting Started
***************

Developing
==========

One Time Setup
--------------

Clone the repository:

.. code-block:: bash

  git clone git@github.com:eduNEXT/platform_plugin_teams.git
  cd platform_plugin_teams

Set up a virtualenv with the same name as the repo and activate it. Here's how
you might do that if you have ``virtualenv`` set up:

.. code-block:: bash

  virtualenv -p python3.8 platform_plugin_teams

Every time you develop something in this repo
---------------------------------------------

Activate the virtualenv. Here's how you might do that if you're using
``virtualenv``:

.. code-block:: bash

  source platform_plugin_teams/bin/activate

Grab the latest code:

.. code-block:: bash

  git checkout main
  git pull

Install/update the dev requirements:

.. code-block:: bash

  make requirements

Run the tests and quality checks (to verify the status before you make any
changes):

.. code-block:: bash

  make validate

Make a new branch for your changes:

.. code-block:: bash

  git checkout -b <your_github_username>/<short_description>

Using your favorite editor, edit the code to make your change:

.. code-block:: bash

  vim ...

Run your new tests:

.. code-block:: bash

  pytest ./path/to/new/tests

Run all the tests and quality checks:

.. code-block:: bash

  make validate

Commit all your changes, push your branch to github, and open a PR:

.. code-block:: bash

  git commit ...
  git push


Using the API
*************

To use the API, you need to have a course with teams enabled. To enable you
need to follow the next steps:

1. **Activate teams in your Open edX instance**

   You must add the ``ENABLE_TEAMS`` in your LMS settings (development or
   production). For example, you can create a YAML plugin with the following
   content:

   .. code-block:: yaml

    name: teams-settings
    version: 0.1.0
    patches:
      openedx-common-settings: |
        FEATURES["ENABLE_TEAMS"] = True

2. **Activate teams app**

   You must create a waffle flag in the Django admin panel. You can access to
   Django Admin panel in the next URL: ``<lms_host>/admin/waffle/flag/``. Then,
   you need to create a new flag with the following values:

   - Name: ``teams.enable_teams_app``
   - Everyone: ``Yes``
   - Superusers: ``True``

Now, you can use the API. All the endpoints are protected with the same auth
method as the Open edX default teams API, and adds a new ``JwtAuthentication``
auth method. For generate a token, you can use the next endpoint:

- POST ``/<lms_host>/oauth2/access_token/``: Generate a token for the user. The
  content type of the request must be ``application/x-www-form-urlencoded``.

  **Body parameters**

  - ``client_id``: Client ID of the OAuth2 application. You can find it in the
    Django admin panel. Normally, it is ``login-service-client-id``.
  - ``grant_type``: Grant type of the OAuth2 application. Normally, it is
    ``password``.
  - ``username``: Username of the user.
  - ``password``: Password of the user.
  - ``token_type``: Type of the token. By default, it is ``bearer`` by default
    but can be ``JWT``.

  **Response**

  - ``access_token``: Access token of the user. You must use this token in the
    ``Authorization`` header of the requests to the API.

Finally, you are ready to use the API. The next endpoints are available:

- GET ``/<lms_host>/platform-plugin-teams/<course_id>/api/topics/``: List all
  the topics in the course.

  **Path parameters**

  - ``course_id``: ID of the course.

  **Query parameters**

  - ``page``: Page number of the results.
  - ``page_size``: Number of results per page.

- POST ``/<cms_host>/platform-plugin-teams/<course_id>/api/topics/``: Create a
  new topic in the course. The content type of the request must be ``application/json``.

  **Path parameters**

  - ``course_id``: ID of the course.

  **Body parameters**

  - ``name``: Name of the topic.
  - ``description``: Description of the topic.
  - ``type``: Type of the topic. It can be ``open``, ``public_managed`` or
    ``private_managed``.
  - ``max_team_size``: Maximum number of members in the teams of the topic.

- DELETE ``/<cms_host>/platform-plugin-teams/<course_id>/api/topics/<topic_id>/``:
  Delete a topic in the course.

  **Path parameters**

  - ``course_id``: ID of the course.
  - ``topic_id``: ID of the topic.

- POST ``/<lms_host>/platform-plugin-teams/<course_id>/api/team-membership/``:
  Add a user to a team. The content type of the request must be ``application/json``.

  **Path parameters**

  - ``course_id``: ID of the course.

  **Body parameters**

  - ``usernames``: List of usernames of the users to add to the team.
  - ``team_id``: ID of the team.


Getting Help
************

If you're having trouble, we have discussion forums at `discussions`_ where you
can connect with others in the community.

Our real-time conversations are on Slack. You can request a
`Slack invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an `issue`_ in this
repository with as many details about the issue you are facing as you
can provide.

For more information about these options, see the `Getting Help`_ page.

.. _discussions: https://discuss.openedx.org
.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _issue: https://github.com/eduNEXT/platform-plugin-teams/issues
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL 3.0 unless otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome. Please read `How To Contribute`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

.. _How To Contribute: https://openedx.org/r/how-to-contribute


Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@edunext.co.

.. It's not required by our contractor at the moment but can be published later
.. .. |pypi-badge| image:: https://img.shields.io/pypi/v/platform-plugin-teams.svg
    :target: https://pypi.python.org/pypi/platform-plugin-teams/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/eduNEXT/platform-plugin-teams/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/eduNEXT/platform-plugin-teams/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/platform-plugin-teams.svg
    :target: https://github.com/eduNEXT/platform-plugin-teams/blob/main/LICENSE.txt
    :alt: License

.. .. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
..  |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
