from multiprocessing import Pool
from babifinance import babifinance, babifinance_alerts
from bibaodao import bibaodao, bibaodao_alerts
from bishequ import bishequ, bishequ_alerts
from bitrating import bitrating, bitrating_alerts
from btc123 import btc123, btc123_alerts
from chainfor import chainfor,  chainfor_alerts
from coingogo import coingogo,  coingogo_alerts
from coinvoice import coinvoice, coinvoice_alerts
from epcnn import epcnn, epcnn_alerts
from fengniaocaijing import fengniaocaijing, fengniaocaijing_alerts
from fn import fn, fn_alerts
from hangliancj import hangliancj, hangliancj_alerts
from hashcaijing import hashcaijing, hashcaijing_alerts
from hecaijing import hecaijing, hecajing_alerts
from huoxing import huoxing24, huoxing_alerts
from ihuoqiu import ihuoqiu, ihuoqiu_alerts
from jinse import jinse, jinse_alerts
from leilook import leilook, leilook_alerts
from longkuai import longkuai, longkuai_alerts
from polo321 import polo321, polo321_alerts
from queding import queding, queding_alerts
from shangxia import shangxia, shangxia_alerts
from shilian import shilian, shilian_alerts
from tuoluocaijing import tuoluocaijing, tuoluocaijing_alerts
from tuoniaox import tuoniaox, tuoniaox_alerts
from weilaicaijing import weilaicaijing, weilaicaijing_alerts
from xinbinews import xinbinews, xinbinews_alerts
from youjiatuanjian import youjiatuanjian, youjiatuanjian_alerts
from zhilianfm import zhilianfm, zhilianfm_alerts
from haitunbc import haitunbc, haitunbc_alerts
from huolian import huolian51, huolian51_alerts
from zaoping import zaoping, zaoping_alerts
from qianba import qianba
from btc798 import btc798, btc798_alerts
from bikuai import bikuai, bikuai_alerts
from budkr import budkr
from gongxiangcj import gongxiangcj, gongxiangcj_alerts
import mongodb_news
import time


def allStart():
    startList = [babifinance.starts, babifinance_alerts.starts, bibaodao.starts, bibaodao_alerts.starts,
                 bishequ.starts, bishequ_alerts.starts, bitrating.starts, bitrating_alerts.starts,
                 btc123.starts, btc123_alerts.starts, chainfor.starts, chainfor_alerts.starts, coingogo.starts,
                 coingogo_alerts.starts, coinvoice.starts, coinvoice_alerts.starts, epcnn.starts, epcnn_alerts.starts,
                 fengniaocaijing.starts, fengniaocaijing_alerts.starts, fn.starts, fn_alerts.starts, hangliancj.starts,
                 hangliancj_alerts.starts, hashcaijing_alerts.starts,
                 hecaijing.starts, hecajing_alerts.starts, huoxing24.starts, huoxing_alerts.starts, ihuoqiu.starts,
                 ihuoqiu_alerts.starts, jinse.starts, jinse_alerts.starts, leilook.starts, leilook_alerts.starts,
                 longkuai.starts, longkuai_alerts.starts, polo321.starts, polo321_alerts.starts, queding.starts,
                 queding_alerts.starts, shangxia.starts, shangxia_alerts.starts, shilian.starts, shilian_alerts.starts,
                 tuoluocaijing.starts, tuoluocaijing_alerts.starts, tuoniaox.starts, tuoniaox_alerts.starts,
                 weilaicaijing.starts, weilaicaijing_alerts.starts,
                 youjiatuanjian.starts, youjiatuanjian_alerts.starts, zhilianfm.starts, zhilianfm_alerts.starts,
                 haitunbc.starts, huolian51.starts, huolian51_alerts.starts, zaoping.starts,
                 zaoping_alerts.starts, qianba.starts, btc798.starts, btc798_alerts.starts, bikuai.starts,
                 bikuai_alerts.stars, budkr.starts, gongxiangcj.starts, gongxiangcj_alerts.starts]
    p = Pool(5)
    for start in startList:
        p.apply_async(start)
    p.close()
    p.join()


if __name__ == '__main__':
    while True:
        allStart()
        mongodb_news.closeMongodb()
        time.sleep(600)
