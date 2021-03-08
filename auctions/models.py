from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', null=True, blank=True)

class Category(models.Model):
    """Model representing a specific auction listing CATEGORY."""

    title = models.CharField(max_length=200, help_text='Enter the title of the category')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the listing', null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.title}'

class Listing(models.Model):
    """Model representing a specific auction LISTING."""

    title = models.CharField(max_length=200, help_text='Enter the title of the listing')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the listing')
    start_bid = models.DecimalField(max_digits=20, decimal_places=2, help_text='Enter the starting bid value')
    image = models.URLField(null=True, blank=True, help_text="Enter bid's image URL")
    category = models.ManyToManyField(Category)
    start_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(User, related_name="winners", on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def current_price(self):
        try:
            return Bid.objects.filter(listing=self).order_by('-value')[0].value
        except:
            return self.start_bid

    @property
    def history(self):
        history = [{
            'time': self.start_date,
            'user': self.owner,
            'event': f'Started listing with bid of {self.start_bid}'
        }]
        bids = Bid.objects.filter(listing=self)
        for bid in bids:
            history += [{
                'time': bid.time,
                'user': bid.owner,
                'event': f'Raised bid to {bid.value}'
            }]
        comments = Comment.objects.filter(listing=self)
        for comment in comments:
            history += [{
                'time': comment.time,
                'user': comment.owner,
                'event': f'Commented: {comment.text}'
            }]
        if self.closed:
            history += [{
                'time': self.closed,
                'user': self.owner,
                'event': f' closed bid and { self.winner } won!'
            }]
        return sorted(history, key=lambda k:k['time'])

    def close(self):
        self.closed = datetime.now()
        bid = Bid.objects.filter(listing=self).order_by('-value')[0]
        if bid: 
            self.winner = bid.owner

    def open(self):
        self.closed = None
        self.winner = None

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.title}'

class Bid(models.Model):
    """Model representing a specific auction listing BID."""

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.RESTRICT)
    value = models.DecimalField(max_digits=20, decimal_places=2, help_text='Enter the bid value')
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.owner != self.listing.owner:
            if self.listing.bid_set.all():
                if self.value > self.listing.current_price:
                    super().save(*args, **kwargs)
            elif self.value >=  self.listing.start_bid:
                super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.value}'

class Comment(models.Model):
    """Model representing a specific auction listing COMMENT."""

    text = models.TextField(max_length=1000, help_text='Enter a brief description of the listing')
    time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.RESTRICT)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.text}'