class MxModelUpdate(object):
    def update_fields(self, **kwargs):
        mx_queryset = self._meta.model.objects.filter(pk=self.pk)
        try:
            mx_queryset.update(
                **{k: v for k, v in kwargs.items() if k in [i.name for i in self._meta.model._meta.get_fields()]})
        except Exception as e:
            raise e

    class Meta:
        proxy = True
