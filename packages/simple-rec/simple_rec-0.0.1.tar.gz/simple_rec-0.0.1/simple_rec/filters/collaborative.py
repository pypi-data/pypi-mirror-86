from typing import List, Union
import numpy as np

from simple_rec.compute._sparse import _SparseMatrix
from simple_rec.compute._sparse import _SparseDecomposeMixin
from simple_rec.compute._similarity import _SimilaritySearchMixin


class _CollaborativeFilter(_SparseMatrix, _SparseDecomposeMixin):
    """Base class for CollaborativeFilter.

    Handles the mapping of users and items to unique indices.

    Attributes:
        n_users:
            Number of unique users.
        n_items:
            Number of unique items.
        user_to_row:
            Mapping from users to rows of the user-item matrix.
        row_to_user:
            Mapping from rows of the user-item matrix to users.
        item_to_col:
            Mapping from items to cols of the user-item matrix.
        col_to_item:
            Mapping from cols of the user-item matrix to items.

    """

    def __init__(self,
                 users: List[Union[int, str]] = [],
                 items: List[Union[int, str]] = [],
                 ratings: List[float] = []):

        self.n_users = 0
        self.n_items = 0
        self.user_to_row = {}
        self.row_to_user = {}
        self.item_to_col = {}
        self.col_to_item = {}

        # initialize mappings from users/items to rows/cols
        for row, user in enumerate(np.unique(users)):
            self.user_to_row[user] = row
            self.row_to_user[row] = user
            self.n_users += 1
        for col, item in enumerate(np.unique(items)):
            self.item_to_col[item] = col
            self.col_to_item[col] = item
            self.n_items += 1

        # initialize sparse matrix representation
        super(_CollaborativeFilter, self).__init__(
            [self.user_to_row[user] for user in users],
            [self.item_to_col[item] for item in items],
            ratings
        )

    def get(self,
            user: Union[int, str],
            item: Union[int, str]):
        """Returns the value of the user-item matrix for (user, item).

        """
        row = self.user_to_row[user]
        col = self.item_to_col[item]
        return self._get(row, col)

    def user_items(self,
                   user: Union[int, str]):
        """Returns all items for a given user.

        """
        row = self.user_to_row[user]
        items = [self.col_to_item[col] for col in self._row(row)]
        return items

    def item_users(self,
                   item: Union[int ,str]):
        """Returns all users for a given item.

        """
        col = self.item_to_col[item]
        users = [self.row_to_user[row] for row in self._col(col)]
        return users

    def add_rating(self,
                   user: Union[int, str],
                   item: Union[int, str],
                   rating: float):
        """Adds an entry to the user-item matrix.

        """
        raise NotImplementedError()


class CollaborativeFilter(_CollaborativeFilter, _SimilaritySearchMixin):
    """Collaborative filter based on a sparse user-item matrix.

    Attributes:
        users:
            All appearances of users in the user-item matrix.
        items:
            All appearances of items in the user-item matrix.
        ratings:
            All ratings of in the user-item matrix.

    Examples:

        In the following example, Alice likes the book "Moby Dick" a lot but she
        cannot stand "To Kill A Mocking Bird". Bob and Chris both do not like 
        "Moby Dick" but have no opinion on "To Kill A Mocking Bird".

        >>> users = ["Alice", "Alice", "Bob", "Chris"]
        >>> items = ["Moby Dick", "To Kill A Mocking Bird", "Moby Dick", "Moby Dick"]
        >>> ratings = [1.0, 0.0, 0.2, 0.1]
        >>>
        >>> # collaborative filter
        >>> collab_filter = CollaborativeFilter(users, items, ratings)
        >>> collab_filter.fit()
        >>> 
        >>> # recommend items based on selected item
        >>> items, agreement = collab_filter.item_to_item("Moby Dick")
        >>>
        >>> # recommend items for a given user
        >>> items, agreement = collab_filter.user_to_item("Bob")
        >>>
        >>> # recommend users with similar taste
        >>> users, agreement = collab_filter.user_to_user("Bob")

    """

    def __init__(self,
                 users: List[Union[int, str]] = [],
                 items: List[Union[int, str]] = [],
                 ratings: List[float] = []):

        self.users = users
        self.items = items
        self.ratings = ratings

        super(CollaborativeFilter, self).__init__(users, items, ratings)

    def fit(self,
            k: int = 16,
            min_iter: int = 5,
            max_iter: int = 30,
            eps: float = 1e-6):
        """Performs sparse matrix decomposition to get user and item embeddings.

        Args:
            k:
                Dimensionality of the embeddings.
            min_iter:
                Minimum iterations of the decomposition algorithm.
            max_iter:
                Maximum iterations of the decomposition algorithm.
            eps:
                Stop iterating if error is smaller than this.

        Returns:
            Mean squared error of the reconstructed matrix.

        """
        mse = self._decompose(self.n_users,
                              self.n_items,
                              k=k,
                              min_iter=min_iter,
                              max_iter=max_iter,
                              eps=eps)
        return mse


    def item_to_item(self,
                     item: Union[int, str],
                     top: int = 1):
        """Finds the top most similar items to the query.

        Args:
            item:
                The query item.
            top:
                Number of items to return.

        Returns:
            The most similar items to the query and the similarity values.

        """
        # check whether there is an entry for item
        item_col = self.item_to_col.get(item, None)
        if item_col is None:
            return [], []

        # compute similarities and neareast neighbors
        cols, similarities = \
            self._cosine_similarity(self.V[item_col], self.V)

        # return only most similar items
        items = [self.col_to_item[col] for col in cols]
        top = min(len(items), top + 1)
        return items[1:top], similarities[1:top]

    def item_to_user(self,
                     item: Union[int, str],
                     top: int = 1):
        """Finds the top most similar users to the query.

        Args:
            item:
                The query item.
            top:
                Number of users to return.

        Returns:
            The most similar users to the query and the similarity values.

        """
        # check whether there is an entry for item
        item_col = self.item_to_col.get(item, None)
        if item_col is None:
            return [], []

        # compute similarities and neareast neighbors
        rows, similarities = \
            self._cosine_similarity(self.V[item_col], self.U)

        # return only most similar users
        users = [self.row_to_user[row] for row in rows]
        top = min(len(users), top)
        return users[:top], similarities[:top]


    def user_to_item(self,
                     user: Union[int, str],
                     top: int = 1):
        """Finds the top most similar items to the query.

        Args:
            user:
                The query user.
            top:
                Number of items to return.

        Returns:
            The most similar items to the query and the similarity values.

        """
        # check whether there is an entry for user
        user_row = self.user_to_row.get(user, None)
        if user_row is None:
            return [], []

        # compute similarities and neareast neighbors
        cols, similarities = \
            self._cosine_similarity(self.U[user_row], self.V)

        # return only most similar items
        items = [self.col_to_item[col] for col in cols]
        top = min(len(items), top)
        return items[:top], similarities[:top]


    def user_to_user(self,
                     user: Union[int, str],
                     top: int = 1):
        """Finds the top most similar users to the query.

        Args:
            users:
                The query users.
            top:
                Number of users to return.

        Returns:
            The most similar users to the query and the similarity values.

        """
        # check whether there is an entry for user
        user_row = self.user_to_row.get(user, None)
        if user_row is None:
            return [], []

        # compute similarities and neareast neighbors
        rows, similarities = \
            self._cosine_similarity(self.U[user_row], self.U)

        # return only the most similar users
        users = [self.row_to_user[row] for row in rows]
        top = min(len(users), top + 1)
        return users[1:top], similarities[1:top]
