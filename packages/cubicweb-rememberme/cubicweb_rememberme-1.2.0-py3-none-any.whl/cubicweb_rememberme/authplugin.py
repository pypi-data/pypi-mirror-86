"""http://fishbowl.pastiche.org/2004/01/19/persistent_login_cookie_best_practice/

:organization: Logilab
:copyright: 2009-2011 LOGILAB S.A. (Paris, FRANCE), license is LGPL v2.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: GNU Lesser General Public License, v2.1 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

from cubicweb import AuthenticationError
from cubicweb.server.sources import native


class AuthCookieAuthentifier(native.BaseAuthentifier):
    auth_rql = ('Any X,AC WHERE X is CWUser, X login %(login)s, '
                'AC auth_cookie_for_user X, AC magic %(magic)s, '
                'AC lifetime L, AC creation_date > (NOW - L)')

    def authenticate(self, session, login, magic=None, **kwargs):
        """return CWUser eid for the given login/cookie if this account is
        defined in this source, else raise `AuthenticationError`
        """
        if magic is None:
            raise AuthenticationError()
        rset = session.execute(self.auth_rql, {'login': login,
                                               'magic': magic})
        if rset:
            session.repo.glob_delete_entities(session, set((rset[0][1],)))
            session.commit()
            return rset[0][0]
        raise AuthenticationError('bad cookie')
