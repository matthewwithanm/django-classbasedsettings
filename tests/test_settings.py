from cbsettings import DjangoDefaults


class A(DjangoDefaults):
    IS_A = True


class B(DjangoDefaults):
    IS_B = True


class Parent(DjangoDefaults):
    PARENT_ATTR = True


class Child(Parent):
    CHILD_ATTR = True
