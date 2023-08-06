
import sys

from types import ModuleType, FunctionType

from gc import get_referents


BLACKLIST = type, ModuleType, FunctionType
def getsize(obj):
    """
    Get a sum of sizes from an object and it's members in bytes.
    Custom objects know their class.
    Function objects seem to know way too much, including modules.
    Exclude modules as well.

    Author: Aaron Hall @ https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
    """
    if isinstance(obj, BLACKLIST):
        # raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
        return sys.getsizeof(obj)
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size


def attributes(obj, properties=True, methods=True, variables=True, modules=False, protected=False, from_instance=True, from_class=True, from_bases=True):
    """ Get attributes from a Module or Class with a lot of optional flags for filtering.

        :param obj:
        :param bool properties:
        :param bool methods:
        :param bool variables:
        :param bool modules:
        :param bool or None protected: Whether to return protected, non-protected or all if None.
        :param bool from_instance: Whether to return attributes only defined in instance.
        :param bool from_class: Whether to return attributes defined in direct class.
        :param bool from_bases: Whether to return attributes defined by an inheritence. """
    if isinstance(obj, type):
        cls = obj
        instance = None
    else:
        cls = obj.__class__
        instance = obj

    attrs = {}
    for key in dir(obj):
        cls_attr = getattr(cls, key, ...)
        is_property = isinstance(cls_attr, property)
        is_protected = key.startswith("_")
        attr = cls_attr if is_property else getattr(obj, key, ...)

        # Attribute is Property, Method and Variable
        if is_property:
            if properties is False:
                continue
        elif callable(attr):
            if methods is False:
                continue
        elif cls.__name__ == "module":
            if modules is False:
                continue
        else:
            if variables is False:
                continue

        # Key is Protected
        if protected is False and is_protected:
            continue
        elif protected is True and not is_protected:
            continue

        # Origin from Instance, Class, Base or Builtin
        if from_instance is False and instance and attr != cls_attr and cls_attr is ...:
            continue
        elif not (from_class and from_bases) and cls_attr is not ...:
            for base in cls.__bases__:
                if getattr(base, key, ...) is not ...:
                    defined_in_base = True
                    break
            else:
                defined_in_base = False

            if from_bases is False and defined_in_base:
                continue
            elif from_class is False and not defined_in_base:
                continue

        attrs[key] = attr
    return attrs

def initBases(cls):
    """
    Decorator function for class to automatically initalize all inherited classes.

    Wrap a class' unbound __init__ method to take any arguments.
    When wrapper is called it iterates DIRECT bases to call their unbound __init__ methods along with it's own original __init__.

    Also looks for defined `_post_init` methods, stores them in `instance._post_inits` and calls them all after all inits.
    """
    cls_init = cls.__init__  # Unbound original __init__ method of class

    def _wrapper(*args, **kwargs):
        cls_SigInfo = SigInfo(cls_init, *args, **kwargs)

        if not cls_SigInfo["self"]:
            raise AttributeError(f"{cls} hasn't defined it's `__init__`")

        initialized_bases = []


        if getattr(cls_SigInfo["self"], "_post_inits", None) is None:
            cls_SigInfo["self"]._post_inits = []


        for base in cls.__bases__ + (cls, ):
            init = cls_init if base is cls else base.__init__

            if init is not object.__init__ and init not in initialized_bases:
                cls_SigInfo(child_callable=init)
                initialized_bases.append(init)


                if getattr(base, "_post_init", None) and base._post_init not in cls_SigInfo["self"]._post_inits:
                    cls_SigInfo["self"]._post_inits.append(base._post_init)
        if cls is cls_SigInfo["self"].__class__ and getattr(cls_SigInfo["self"], "_post_inits", None) is not None:
            for post_init in cls_SigInfo["self"]._post_inits:
                cls_SigInfo(child_callable=post_init)


    cls.__init__ = _wrapper
    return cls

from generallibrary.functions import SigInfo


































