
class AvtoProSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'avtopro'
        ]


default = AvtoProSettings
