"""rememberme components: plug authentication retriever

:organization: Logilab
:copyright: 2009-2012 LOGILAB S.A. (Paris, FRANCE), license is LGPL v2.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: GNU Lesser General Public License, v2.1 - http://www.gnu.org/licenses
"""
from datetime import date, timedelta

from six import text_type

from cubicweb import Unauthorized, _
from cubicweb.utils import make_uid
from cubicweb.predicates import is_instance
from cubicweb.web import formfields as ff, formwidgets as fw
from cubicweb.web.views import (authentication, basecontrollers, basetemplates,
                                autoform, actions, uicfg)

_pvs = uicfg.primaryview_section
_pvs.tag_object_of(('CWAuthCookie', 'auth_cookie_for_user', 'CWUser'), 'hidden')

_abaa = uicfg.actionbox_appearsin_addmenu
_abaa.tag_object_of(('CWAuthCookie', 'auth_cookie_for_user', 'CWUser'), False)

# web authentication info retriever ############################################


class AuthCookieRetriever(authentication.WebAuthInfoRetriever):
    """authenticate by a magic identifier stored a cookie on the client host
    """
    __regid__ = 'magicnumauth'
    order = 0

    def __init__(self, vreg):
        # XXX make lifetime configurable
        self.cookie_lifetime = timedelta(days=30)

    def authentication_information(self, req):
        """retrieve authentication information from the given request, raise
        NoAuthInfo if expected information is not found:

        return info from long lived authentication cookie if any
        """
        cookie = req.get_cookie()
        try:
            authcookie = cookie['__cw_auth_cookie'].value
        except KeyError:
            raise authentication.NoAuthInfo()
        if not isinstance(authcookie, text_type):
            authcookie = authcookie.decode('ascii')
        try:
            login, magic = authcookie.split('|__magic=', 1)
        except ValueError:
            req.remove_cookie('__cw_auth_cookie')
            raise authentication.NoAuthInfo()
        return login, {'magic': magic}

    def cleanup_authentication_information(self, req):
        req.remove_cookie('__cw_auth_cookie')

    def authenticated(self, retriever, req, session, login, authinfo):
        """callback when return authentication information have opened a
        repository connection successfully. Take care req has no session
        attached yet, hence req.execute isn't available.

        Here we set authentication cookie for the next time
        """
        if not (retriever is self or '__setauthcookie' in req.form):
            return
        req.form.pop('__setauthcookie', None)
        user = session.user
        cls = req.vreg['etypes'].etype_class('CWAuthCookie')
        #  req has no session set yet
        with session.new_cnx() as cnx:
            authentity = cls.cw_instantiate(cnx.execute,
                                            magic=text_type(make_uid()),
                                            lifetime=self.cookie_lifetime,
                                            auth_cookie_for_user=user.eid)
            cnx.commit()
        # we've to commit here, else cookie may be rollbacked by errors while
        # trying to set last_login_time in the CookieSessionHandler (eg for ldap
        # user at least).
        magic = authentity.magic
        value = '%s|__magic=%s' % (user.login, magic)
        req.set_cookie('__cw_auth_cookie', value, maxage=None,
                       expires=date.today() + self.cookie_lifetime)
        authinfo['magic'] = magic

    def request_has_auth_info(self, req):
        cookie = req.get_cookie()
        try:
            authcookie = cookie['__cw_auth_cookie'].value
        except KeyError:
            return False
        try:
            login, magicnum = authcookie.split('|__magic=', 1)
        except ValueError:
            req.remove_cookie('__cw_auth_cookie')
            return False
        if not (login and magicnum):
            req.remove_cookie('__cw_auth_cookie')
            return False
        return True

    def revalidate_login(self, req):
        cookie = req.get_cookie()
        authcookie = cookie['__cw_auth_cookie'].value
        return authcookie.split('|__magic=', 1)[0]


# add remember me checkbox on the login form ###################################

basetemplates.LogForm.append_field(
    ff.BooleanField(name='__setauthcookie', choices=[(u'', u'1')],
                    label=_('remember me'), widget=fw.CheckBox({'class': 'data'}))
)


# deactivate manual addition/edition ###########################################

class UneditableCWAuthCookieEdition(autoform.AutomaticEntityForm):
    __select__ = is_instance('CWAuthCookie')

    def __init__(self, *args, **kwargs):
        raise Unauthorized()


actions.ModifyAction.__select__ = actions.ModifyAction.__select__ & ~is_instance('CWAuthCookie')
actions.MultipleEditAction.__select__ = actions.MultipleEditAction.__select__ & ~is_instance(
    'CWAuthCookie')


class LogoutController(basecontrollers.LogoutController):

    def publish(self, rset=None):
        """logout from the instance"""
        cookie = self._cw.get_cookie()
        if '__cw_auth_cookie' in cookie:
            self._cw.remove_cookie('__cw_auth_cookie')
        try:
            # removing all existing auth cookie entities, not only the currently
            # used one, doesn't seem like a bad idea
            self._cw.execute('DELETE CWAuthCookie X '
                             'WHERE X auth_cookie_for_user U, U eid %(u)s',
                             {'u': self._cw.user.eid})
            self._cw.cnx.commit()
        except Exception:
            self.exception('error while deleting authentication cookie for %s',
                           self._cw.user.login)
        return super(LogoutController, self).publish(rset)


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (LogoutController,))
    vreg.register_and_replace(LogoutController, basecontrollers.LogoutController)
