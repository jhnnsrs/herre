from typing import Type
from pydantic.main import BaseModel, ModelMetaclass

from herre.wards.graphql import GraphQLWard, ParsedQuery
from herre.wards.registry import get_ward_registry


class QueryMeta(ModelMetaclass):
    """
    The Model Meta class extends the Pydantic Metaclass and adds in
    syncrhonous and asynchronous Managers. These Managers allow direct
    interaction with serverside Objects mimicking the Django ORM Scheme
    (https://docs.djangoproject.com/en/3.2/topics/db/queries/) it
    also registeres the Model as a potential serializer.

    Every Class using this metaclass has to subclass pydantic.BaseModel and
    implement a Meta class with the identifier attribute set to a cleartext
    identifier on the arkitekt platform.

    If this identifier does not exist, the serializer can potentially be auto
    registered with the platform according to the apps name

    Args:
        ModelMetaclass ([type]): [description]
    """

    def __new__(mcls, name, bases, attrs):
        slots = set(
            attrs.pop("__slots__", tuple())
        )  # The slots from: https://github.com/samuelcolvin/pydantic/issues/655#issuecomment-610900376
        for base in bases:
            if hasattr(base, "__slots__"):
                slots.update(base.__slots__)

        if "__dict__" in slots:
            slots.remove("__dict__")
        attrs["__slots__"] = tuple(slots)

        return super(QueryMeta, mcls).__new__(mcls, name, bases, attrs)

    @property
    def get_meta(cls):
        return cls.__meta

    @property
    def ward(cls) -> GraphQLWard:
        return get_ward_registry().get_ward_instance(cls.__meta.ward)

    def __init__(self, name, bases, attrs):
        super(QueryMeta, self).__init__(name, bases, attrs)
        if attrs["__qualname__"] != "Model":
            # This gets allso called for our Baseclass which is abstract
            self.__meta = attrs["Meta"] if "Meta" in attrs else None
            assert (
                self.__meta is not None
            ), f"Please provide a Meta class in your Arnheim Model {name}"

            try:
                if self.__meta.abstract:
                    return
            except:
                pass

            register = getattr(self.__meta, "register", True)
            assert hasattr(
                self.__meta, "ward"
            ), f"Please specifiy which Ward this Model should use in Meta of  {attrs['__qualname__']}"

            assert hasattr(
                self.__meta, "document"
            ), f"Please specifiy the document to use for this Operation in Meta document"

            if register:
                self.register_model(meta=self.__meta)


class Model(BaseModel, metaclass=QueryMeta):
    """Model

    Model is the abstract baseclass of all Serverside Models and provides a Django ORM
    like interface for retrieving data from the Server.

    Implements:
        id (str): Every Model has an id (UUID) that identifies the Server Instance

    Args:
        BaseModel ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to ModelMeta.

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """


class GraphQLQuery(BaseModel, metaclass=QueryMeta):
    @classmethod
    def register_model(cls, **kwargs):
        """Will be invoked by the meta class and will make this model
        register with other models if wanted

        Returns:
            [type]: [description]
        """
        return None

    @classmethod
    def query(cls, variables):
        data = cls.ward.run(query=ParsedQuery(cls.Meta.document), variables=variables)
        return cls(**data)

    class Meta:
        abstract = True
