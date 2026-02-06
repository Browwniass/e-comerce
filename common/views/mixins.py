from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ExtendedGenericViewSet(GenericViewSet):
    pass


class LCRDViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    pass


class LCRUViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    pass


class LCRUDViewSet(
    LCRUViewSet,
    mixins.DestroyModelMixin,
):
    pass
