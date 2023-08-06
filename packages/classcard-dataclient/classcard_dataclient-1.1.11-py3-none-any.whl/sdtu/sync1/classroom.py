from sync1.base import BaseSync
from requester.sdtu import SDTURequester
from config import SDTU_PAGE_SIZE
from utils.loggerutils import logging
from utils.code import get_md5_hash
from classcard_dataclient.models.classroom import Classroom, RoomType

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def __init__(self):
        super(ClassroomSync, self).__init__()
        self.sdtu_requester = SDTURequester()
        self.classroom_map = {}
        self.yjs_classroom_map = {}
        self.bks_classroom_map = {}

    def analyse_building(self, classroom_name):
        building, floor = None, None
        if classroom_name:
            key_words = ["楼", "区", "座"]
            for kw in key_words:
                if kw in classroom_name:
                    kw_index = classroom_name.index(kw)
                    building = classroom_name[:kw_index + 1]
                    try:
                        cur = -1
                        for _ in range(len(classroom_name)):
                            if classroom_name[cur].isdigit():
                                floor = str(int(classroom_name[cur - 2]))
                                break
                            cur -= 1
                    except (Exception,):
                        pass
                    break
        return building, floor, None

    def extract_bks_classroom(self):
        page_index = 1
        while True:
            classroom_res = self.sdtu_requester.get_bks_classroom_list(page=page_index, pagesize=SDTU_PAGE_SIZE)
            total_count = classroom_res["total"]
            current_rows = classroom_res["data"]["Rows"]
            for d in current_rows:
                campus, number, name = d["XQMC"], d["JSDM"], d["JSMC"]
                classroom_num = get_md5_hash(number)
                building, floor, _ca = self.analyse_building(name)
                if classroom_num not in self.classroom_map:
                    self.classroom_map[classroom_num] = Classroom(number=classroom_num, name=name,
                                                                  building=building, floor=floor,
                                                                  category=RoomType.TYPE_PUBLIC,
                                                                  extra_info={'campus': campus})
                    self.bks_classroom_map[name] = classroom_num
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1

    def extract_yjs_classroom(self):
        page_index = 1
        while True:
            classroom_res = self.sdtu_requester.get_yjs_classroom_list(page=page_index, pagesize=SDTU_PAGE_SIZE)
            total_count = classroom_res["total"]
            current_rows = classroom_res["data"]["Rows"]
            for d in current_rows:
                campus, number, name, yjs_number = d["XQMC"], d["DZ"], d["DZ"], d["JSBH"]
                classroom_num = get_md5_hash(number)
                building, floor, _ca = self.analyse_building(number)
                if classroom_num not in self.classroom_map:
                    self.classroom_map[classroom_num] = Classroom(number=classroom_num, name=name,
                                                                  building=building, floor=floor,
                                                                  category=RoomType.TYPE_PUBLIC,
                                                                  extra_info={'campus': campus})
                    self.yjs_classroom_map[yjs_number] = classroom_num
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1

    def sync(self):
        self.extract_bks_classroom()
        self.extract_yjs_classroom()
        classrooms = list(self.classroom_map.values())
        self.client.create_classrooms(self.school_id, classrooms)
