Module frontend.RootRequired
============================
A tool to check program permission and if it haven't root permission, die the program

Variables
---------

    
`is_testing`
:   this variable will be True in testing environment to disable root permission check
    (root permission in not needed in testing environment)

Functions
---------

    
`require_root_permission(is_cli=True, die_action=None)`
:   checks root premission.
    If `is_cli` argument is True, when user have not root permission,
    error will print in terminal. but if is False,
    the `die_action` will run as a function.
    (will be disable in testing environment)