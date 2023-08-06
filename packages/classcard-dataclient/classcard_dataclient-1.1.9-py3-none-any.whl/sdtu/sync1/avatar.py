import cx_Oracle
import datetime
from sync.base import BaseSync
from config import AVATAR_ORACLE_SERVER
from utils.loggerutils import logging
import traceback

logger = logging.getLogger(__name__)


class AvatarSync(BaseSync):
    def __init__(self):
        super(AvatarSync, self).__init__()
        self.conn = cx_Oracle.connect(AVATAR_ORACLE_SERVER, encoding="UTF-8", nencoding="UTF-8")  # 连接数据库
        now = datetime.datetime.now()
        self.offset = 300
        self.cur = self.conn.cursor()

    @property
    def last_modify(self):
        return None

    @classmethod
    def write_file(cls, data, filename):
        with open(filename, 'wb') as f:
            f.write(data)
            f.close()

    def extract_avatar(self):
        try:
            if self.last_modify:
                count_sql = "SELECT COUNT(*) FROM T_YKT_PHOTO WHERE ZHXGSJ <= {}".format(self.last_modify)
            else:
                count_sql = "SELECT COUNT(*) FROM T_YKT_PHOTO"
            self.cur.execute(count_sql)
            try:
                total = self.cur.fetchall()[0][0]
            except (Exception,):
                total = 1
            total_page = total // self.offset if total % self.offset == 0 else total // self.offset + 1
            for index in range(total_page):
                si, ei = index * self.offset + 1, (index + 1) * self.offset
                sql = "SELECT k.XGH, k.XM, k.ZP, k.ZHXGSJ, k.r " \
                      "FROM (SELECT x.*, rownum r FROM T_YKT_PHOTO x " \
                      "WHERE ZHXGSJ <= {} ORDER BY XGH) " \
                      "k WHERE k.r BETWEEN {} and {}".format(self.last_modify, si, ei)
                self.cur.execute(sql)
                rows = self.cur.fetchall()
                for row in rows:
                    number, name, avatar = row[0], row[1], row[2]
                    if not (number and avatar):
                        continue
        except (Exception,):
            logger.error(traceback.format_exc())
        finally:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()

    def sync(self):
        pass