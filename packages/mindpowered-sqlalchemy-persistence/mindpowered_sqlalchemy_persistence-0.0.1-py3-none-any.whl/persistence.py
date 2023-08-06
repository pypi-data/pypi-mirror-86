import maglev

class Persistence:
	def __init__(self, bus):
		self.pybus = maglev.maglev_MagLevPy(bus)
		self.pybus.register('Persistence.EnglishAuction.Auction.CreateNew', self.Persistence_EnglishAuction_Auction_CreateNew)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindById', self.Persistence_EnglishAuction_Auction_FindById)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindStarting', self.Persistence_EnglishAuction_Auction_FindStarting)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindEnding', self.Persistence_EnglishAuction_Auction_FindEnding)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindOpen', self.Persistence_EnglishAuction_Auction_FindOpen)
		self.pybus.register('Persistence.EnglishAuction.Bid.CountForAuction', self.Persistence_EnglishAuction_Bid_CountForAuction)
		self.pybus.register('Persistence.EnglishAuction.Bid.FindByHighestPriceForAuction', self.Persistence_EnglishAuction_Bid_FindByHighestPriceForAuction)
		self.pybus.register('Persistence.EnglishAuction.Bid.New', self.Persistence_EnglishAuction_Bid_New)
	def Persistence_EnglishAuction_Auction_CreateNew(args):
		return "123"
	def Persistence_EnglishAuction_Auction_FindById(args):
		return null
	def Persistence_EnglishAuction_Auction_FindStarting(args):
		return null;
	def Persistence_EnglishAuction_Auction_FindEnding(args):
		return null
	def Persistence_EnglishAuction_Auction_FindOpen(args):
		return null
	def Persistence_EnglishAuction_Bid_CountForAuction(args):
		return null
	def Persistence_EnglishAuction_Bid_FindByHighestPriceForAuction(args):
		return null
	def Persistence_EnglishAuction_Bid_New(args):
		return null
