import fn.fn
import fn.fn_alerts
import hecaijing.hecaijing
import hecaijing.hecajing_alerts
import huoxing.huoxing24
import huoxing.huoxing_alerts
import jinse.jinse
import jinse.jinse_alerts
import youjiatuanjian.youjiatuanjian
import youjiatuanjian.youjiatuanjian_alerts
import threading

def allStart():
    t1 = threading.Thread(target=fn.fn.starts)
    t2 = threading.Thread(target=fn.fn_alerts.starts)
    t3 = threading.Thread(target=hecaijing.hecaijing.starts)
    t4 = threading.Thread(target=hecaijing.hecajing_alerts.starts)
    t5 = threading.Thread(target=huoxing.huoxing24.starts)
    t6 = threading.Thread(target=huoxing.huoxing_alerts.starts)
    t7 = threading.Thread(target=jinse.jinse.starts)
    t8 = threading.Thread(target=jinse.jinse_alerts.starts)
    t9 = threading.Thread(target=youjiatuanjian.youjiatuanjian.starts)
    t10 = threading.Thread(target=youjiatuanjian.youjiatuanjian_alerts.starts)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()


if __name__ == '__main__':
    allStart()