from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import UserBook

@receiver([post_save, post_delete], sender=UserBook)
async def update_book_score(sender, instance, **kwargs):
    """
    Recalculate and persist the average rating whenever a UserBook is saved or deleted.
    """
    book = instance.book
    agg = await book.reviews.aaggregate(avg=Avg('rating'))
    book.score = agg['avg'] or 0
    await book.asave(update_fields=['score'])
