class Reddit:
    def __init__(self, content, title, upvote_ratio,
                 total_awards, score, downvotes, created_at, nsfw, pinned):
        self.content = content
        self.title = title
        self.upvote_ratio = upvote_ratio
        self.total_awards = total_awards
        self.score = score
        self.downvotes = downvotes
        self.created_at = created_at
        self.nsfw = nsfw
        self.pinned = pinned
