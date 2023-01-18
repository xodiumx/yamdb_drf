from rest_framework import mixins, viewsets


class CustomMixinSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,):
    pass
