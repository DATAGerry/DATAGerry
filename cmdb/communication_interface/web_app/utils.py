from math import ceil


class Pagination:
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or (num > self.page - left_current - 1 < self.page + right_current) or \
                            num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def url_for_other_page(page):
    from flask import request, url_for
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

'''
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.cookies:
            token = request.cookies.get('access-token')
        else:
            return redirect(url_for('static_pages.login_page'))
        try:
            token_manager.validate_token(token)
        except TokenVerificationFailed:
            return redirect(url_for('static_pages.login_page'))
        except ExpiredSignatureError:
            return redirect(url_for('static_pages.login_page'))

        return f(*args, **kwargs)
    return decorated
'''
'''
def right_required(required_right):
    
    See Also: https://stackoverflow.com/questions/5929107/decorators-with-parameters
              https://www.artima.com/weblogs/viewpost.jsp?thread=240845
    def page_right(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from cmdb.user_management import user_manager
            token_payload = token_manager.get_payload(request.cookies.get('access-token'))
            user = user_manager.get_user_by_id(token_payload['public_id'])
            try:
                user_manager.user_has_right(user, required_right)
            except UserHasNotRequiredRight as unr:
                application_logger.warning(unr.message)
                abort(403)
                return redirect(url_for('static_pages.error_404_page'))
            return f(*args, **kwargs)
        return decorated
    return page_right
'''