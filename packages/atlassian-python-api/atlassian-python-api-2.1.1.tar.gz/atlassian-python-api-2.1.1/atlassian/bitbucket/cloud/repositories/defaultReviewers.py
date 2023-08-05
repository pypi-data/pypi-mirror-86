# coding=utf-8

from requests import HTTPError

from ..base import BitbucketCloudBase


class DefaultReviewers(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(DefaultReviewers, self).__init__(url, *args, **kwargs)

    def _get_object(self, data):
        if "errors" in data:
            return
        return DefaultReviewer(data, **self._new_session_args)

    def add(self, user):
        """
        Adds the specified user to the repository"s list of default reviewers.

        This method is idempotent. Adding a user a second time has no effect.

        :param user: string: The user to add

        :return: The added DefaultReviewer object
        """
        # the mention_id parameter is undocumented but if missed, leads to 400 statuses
        return self._get_object(self.put(user, data={"mention_id": user}))

    def each(self, q=None, sort=None):
        """
        Returns the repository"s default reviewers.
        These are the users that are automatically added as reviewers on every new pull request
        that is created.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the DefaultReviewer objects
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for default_reviewer in self._get_paged(None, params=params):
            yield self._get_object(default_reviewer)

        return

    def get(self, user):
        """
        Returns the default reviewer in this repository.

        :param user: string: The requested user name

        :return: The requested DefaultReviewer object, None if not a default reviewer
        """
        default_reviewer = None
        try:
            default_reviewer = self._get_object(super(DefaultReviewers, self).get(user))
        except HTTPError as e:
            # A 404 indicates that that specified user is not a default reviewer.
            if not e.response.status_code == 404:
                # Rethrow the exception
                raise

        return default_reviewer


class DefaultReviewer(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(DefaultReviewer, self).__init__(None, *args, data=data, expected_type="user", **kwargs)

    @property
    def display_name(self):
        return str(self.get_data("display_name"))

    @property
    def nickname(self):
        return self.get_data("nickname")

    @property
    def account_id(self):
        return self.get_data("account_id")

    @property
    def uuid(self):
        return self.get_data("uuid")

    def delete(self):
        """
        Deletes the default reviewer
        """
        return super(DefaultReviewer, self).delete(self.url, absolute=True)
