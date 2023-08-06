`Tutor <https://docs.tutor.overhang.io>`__ license management plugin
====================================================================

This is a plugin for `Tutor Wizard Edition <https://overhang.io/tutor/>`__ customers. Running this plugin requires a valid license key. An Wizard Edition subscription provides access to exclusive Tutor plugins.


Installation
------------

This plugin requires a working installation of Tutor. To install Tutor, please check the `official installation instructions <https://docs.tutor.overhang.io/install.html>`__.

Then, install and enable the plugin with::

    pip install tutor-license
    tutor plugins enable license

Quickstart
----------

Obtain a Tutor Wizard Edition license at https://overhang.io/tutor/subscribe. Then, find your license ID and run::

    tutor license save <yourlicenseid>

Your license can only be used on a limited number of computers. Any activated computer can be deactivated at any time, but beware: you will not be able to re-activate it later.

To activate your license, run::

    tutor license users activate

You can then install Tutor Wizard Edition plugins by running ``tutor license install``. For instance::

    tutor license install tutor-monitor

The plugin should now appear in the plugin list::

    tutor plugins list

Note that to start using Wizard Edition plugins, you will have to install Tutor from source, and not by downloading the Tutor binary. You will also need to install ``pip`` for Python 3+. To do so, follow the `official instructions <https://pip.pypa.io/en/stable/installing/>`__.

Once a plugin has been installed, you need to enable it to start using it. For instance::

    tutor plugins enable monitor
    tutor local quickstart

How-to guides
-------------

Storing the Tutor licenses in a different location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the license file is stored in the ``~/.config/tutorlicense/license.json`` file on Linux, and ``~/Library/Application Support/tutorlicense/license.json`` on Mac OS. To specify a different location, use the ``--license-path`` option::

    tutor license --license-path=/your/custom/path/license.json ...

Alternatively, define the following environment variable::

    export TUTOR_LICENSE_PATH=/your/custom/path/license.json
    tutor license ...

Managing ephemeral machines
---------------------------

You may want to deactivate the license associated to a production machine that was terminated. This is frequent in cloud environments. It is possible to do so by setting specific properties to this machine. For instance, on the production machine, before it was terminated, run::

    tutor license users activate --name=myinstance

Then, after it was terminated, fetch its id from another machine with::

    tutor license users list --name=myinstance

Use this ID to deactivate it::

    tutor license users deactivate --id=<myinstanceid>

Or in a single command, with no confirmation prompt::

    tutor license users deactivate --yes \
        --id=$(tutor license users list --name=myinstance --format="{id}")

License
-------

All rights reserved to SASU NULI NULI.