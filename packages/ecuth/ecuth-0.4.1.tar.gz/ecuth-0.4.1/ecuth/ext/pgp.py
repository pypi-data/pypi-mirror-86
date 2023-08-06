# standard imports
import logging
import tempfile

# third-party imports
import gnupg

# local imports
from ecuth.challenge import ChallengeRetriever

logg = logging.getLogger()


class PGPRetriever(ChallengeRetriever):


    def __init__(self, fetcher, parser, gnupg_home=None):
        super(PGPRetriever, self).__init__(fetcher, parser, self._fingerprint_from_challenge_response)
        self.gpg = gnupg.GPG(gnupghome=gnupg_home)


    def _fingerprint_from_challenge_response(self, challenge, signature):
        logg.debug('>>>>>> resolve {}'.format(challenge))
        fn = tempfile.mkstemp()
        f = open(fn[1], 'wb')
        f.write(signature)
        f.close()

        v = None
        try: 
            v = self.gpg.verify_data(fn[1], challenge)
        except Exception as e:
            logg.error('error verifying {}'.format(e))
            return None

        if not v.valid:
            logg.error('signature not value {}'.format(v.key_id))
            return None

        logg.debug('v is {}'.format(v.valid)) 
        #return bytes.fromhex(v.fingerprint)
        return bytes.fromhex(v.key_id)
