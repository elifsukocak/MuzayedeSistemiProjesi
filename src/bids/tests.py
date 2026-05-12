from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from auction.models import Auction
from auction.services import place_bid
from products.models import Urun
from .models import Bid, BidIncrement, BidStatusNotification


class BidServiceTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.satici = User.objects.create_user(
            username='satici',
            password='testpass123',
            role='satici',
            tc_kimlik='11111111111',
        )
        self.musteri1 = User.objects.create_user(
            username='musteri1',
            password='testpass123',
            role='musteri',
            tc_kimlik='22222222222',
        )
        self.musteri2 = User.objects.create_user(
            username='musteri2',
            password='testpass123',
            role='musteri',
            tc_kimlik='33333333333',
        )
        self.urun = Urun.objects.create(
            satici=self.satici,
            ad='Test Urun',
            aciklama='Aciklama',
            baslangicFiyati=Decimal('100.00'),
            durum='aktif',
        )
        self.auction = Auction.objects.create(
            product=self.urun,
            bitis_zamani=timezone.now() + timezone.timedelta(days=1),
            mevcut_fiyat=Decimal('100.00'),
        )
        BidIncrement.objects.create(auction=self.auction, artis_adimi=Decimal('10.00'))
    
    def test_bid_must_follow_increment_step(self):
        mesaj = place_bid(self.musteri1, self.auction, Decimal('105.00'))

        self.assertIn('en az 110.00', mesaj)
        self.assertEqual(Bid.objects.count(), 0)