***************
UserModel Management
***************

Local Users and Groups
======================
Local users and groups can be configured in the WebUI under "Settings" -> "UserModel Management". A user is part of one
group. Access rights are defined for a specific group.

The following groups are defined by default and cannot be deleted:

 * Administrator
 * UserModel

Also, a user cannot delete itself.


Access Rights
=============
Access Rights can be configured for a usergroup and are designed hierachically. Please see the following example::

    # base right for whole application
    base.*

    # right for core framework
    base.framework.*

    # right for accessing objects
    base.framework.object.*

    # right for viewing objects
    base.framework.object.view

    # right for adding objects
    base.framework.object.add

If you add the right "base.framework.object.view" to a usergroup, all users of that group have the right of viewing
objects. If the right "base.framework.object.*" is applied, all subsequent rights like "base.framework.object.view" are
also applied.

A list of rights can be found in the WebUI of DATAGERRY.

The following rights are necessary to use the frontend::

    base.framework.object.view
    base.framework.type.view
    base.framework.category.view
    base.framework.log.view
    base.user-management.user.view
    base.user-management.group.view
    base.docapi.template.view



