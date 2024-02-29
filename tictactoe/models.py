from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

# Create your models here.

class Player(AbstractUser):
    def get_match_statistics(self):

        player_one_wins = self.player_one_matches.filter(winner=self).count()
        player_one_losses = self.player_one_matches.filter(loser=self).count()
        player_one_draws = self.player_one_matches.filter(Q(player_two=self, is_draw=True) | Q(player_one=self, is_draw=True)).count()

        player_two_wins = self.player_two_matches.filter(winner=self).count()
        player_two_losses = self.player_two_matches.filter(loser=self).count()
        player_two_draws = self.player_two_matches.filter(Q(player_two=self, is_draw=True) | Q(player_one=self, is_draw=True)).count()

        total_wins = player_one_wins + player_two_wins
        total_losses = player_one_losses + player_two_losses
        total_draws = player_one_draws + player_two_draws

        statistics = {
            'wins': total_wins,
            'losses': total_losses,
            'draws': total_draws
        }

        return statistics

class Match(models.Model):
    player_one = models.ForeignKey(
        Player, on_delete=models.PROTECT, related_name="player_one_matches"
    )
    player_two = models.ForeignKey(
        Player, on_delete=models.PROTECT, related_name="player_two_matches"
    )
    is_draw = models.BooleanField()
    winner = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="winner_matches",
    )
    loser = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="loser_matches",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
