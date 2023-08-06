

class CategorySettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['categories']
