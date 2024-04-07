from datetime import date
from typing import List, Optional, Set


class Bookmark:
    """
    Bookmark domain model. Note, this is much simpler than P&G's domain model.
    """

    def __init__(self, id, title, url, notes, date_added):
        self.id = None
        self.title = None
        self.url = None
        self.notes = None
        self.date_added = None

        def __str__(self):
            return f"{self.title}"
