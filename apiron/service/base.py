from functools import partial

from apiron.client import ServiceCaller
from apiron.endpoint import Endpoint, StubEndpoint


class ServiceMeta(type):
    @property
    def required_headers(cls):
        return cls().required_headers

    def __getattribute__(cls, *args):
        attribute = type.__getattribute__(cls, *args)
        if isinstance(attribute, Endpoint) or isinstance(attribute, StubEndpoint):
            attribute.callable = partial(ServiceCaller.call, cls, attribute)
        return attribute

    def __str__(cls):
        return str(cls())

    def __repr__(cls):
        return repr(cls())


class ServiceBase(metaclass=ServiceMeta):
    required_headers = {}

    @classmethod
    def get_hosts(cls):
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return []


class Service(ServiceBase):
    """
    A base class for low-level services.

    A service has a domain off of which one or more endpoints stem.
    """

    @classmethod
    def get_hosts(cls):
        """
        The fully-qualified hostnames that correspond to this service.
        These are often determined by asking a load balancer or service discovery mechanism.

        :return:
            The hostname strings corresponding to this service
        :rtype:
            list
        """
        return [cls.domain]

    def __str__(self):
        return self.__class__.domain

    def __repr__(self):
        return "{klass}(domain={domain})".format(klass=self.__class__.__name__, domain=self.__class__.domain)
