from models.player_group import player_group
from config import get_DB_URL

test = player_group(get_DB_URL())
test.insert_to({
  'GAME_ID': 1,
  'PLER_ID': 1,
  'WRKR_ID': 1,
  'PLER_GRP_NM': 'N',
  'GRP_CLSS_TP': 'N'
})