from cbsettings import DjangoDefaults
from cbsettings.switching import Switcher


class A(DjangoDefaults):
    IS_A = True


class B(DjangoDefaults):
    IS_B = True


class Parent(DjangoDefaults):
    PARENT_ATTR = True


class Child(Parent):
    CHILD_ATTR = True


# Used to verify hostnames check
switcher_a = Switcher()
switcher_a.register(B, hostnames=['notamatch'])
switcher_a.register(A, hostnames=['testhost'])
switcher_a.register(B, hostnames=['alsonotamatch'])

# Used to verify NoMatchingSettings errors
switcher_b = Switcher()

# A switcher used to test simple checks
switcher_c = Switcher()
switcher_c.register(B, hostnames=['notamatch'])
switcher_c.register(A, True)
switcher_c.register(B, hostnames=['testhost'])

# A switcher used to test simple callable checks
switcher_d = Switcher()
switcher_d.register(B, hostnames=['notamatch'])
switcher_d.register(A, lambda: True)
switcher_d.register(B, hostnames=['testhost'])
