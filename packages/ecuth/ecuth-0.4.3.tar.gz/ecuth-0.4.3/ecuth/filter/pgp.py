# standard logging
import logging

# third-party imports
import gnupg

logg = logging.getLogger()


class PGPFilter:

    def filter(self, s):
        logg.debug('pgp filter: {}'.format(s))
        return s
