import random
import re
import time

from utils.datachoice import xz
from utils.random import unicode
from utils.mytestcase import MyTestCase
from utils.logincookie import DengLuPage
from utils.screenshort import get_screenshort


class MfSbTest(MyTestCase):
    """搜索查询测试集"""

    def test_trademark_search(self):
        """搜索详情测试"""
        dl = DengLuPage(self.driver)
        dl.login()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#serch-word").click()
        # 获取打开的多个窗口句柄
        windows = self.driver.window_handles
        # 切换到当前最新打开的窗口
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        self.assertIn("注册商标查询_中国商标查询_权大师官网", self.driver.title)
        print(self.driver.title)
        dl.refresh()
        ss = "DD"
        print("搜索商标名称：" + ss)
        self.driver.find_element_by_name("key").send_keys("{}".format(ss))
        self.driver.find_element_by_css_selector("#btnSearchkey").click()
        time.sleep(4)
        print(self.driver.title)

        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        number = random.randint(1, 20)
        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child({}) > div.result-href".format(
                number)).text
        print(str(info).replace("\n", " "))
        self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child({}) > div.result-href".format(
                number)).click()

        windows = self.driver.window_handles
        # 切换到当前最新打开的窗口
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        print(self.driver.current_url)

        brand_info = self.driver.find_element_by_css_selector(
            "#searchDetail > div.page-brand > div > div.brand-left > div.brand-info").text
        print(str(brand_info).replace("\n", " "))

        get_screenshort(self.driver, "test_trademark_search.png")
        print("商标搜索测试通过")

    def test_trademark_hot_1(self):
        """商标热搜测试"""
        dl = DengLuPage(self.driver)
        dl.login()
        time.sleep(2)
        rs1 = self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dt > span.hot-search-item").text
        print("热搜商标_1:" + str(rs1).replace("\n", " "))
        self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dd").click()
        time.sleep(2)
        rs2 = self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dt > span.hot-search-item").text
        print("热搜商标_2:" + str(rs2).replace("\n", " "))
        self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dd").click()
        time.sleep(2)
        rs3 = self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dt > span.hot-search-item").text
        print("热搜商标_3:" + str(rs3).replace("\n", " "))
        get_screenshort(self.driver, "test_trademark_hot_1.png")
        print("热搜正常,测试通过!")

    def test_trademark_hot_2(self):
        """热搜跳转测试"""
        dl = DengLuPage(self.driver)
        dl.login()
        time.sleep(2)
        rs = self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dt > span.hot-search-item").text
        print("热搜商标:" + str(rs).replace("\n", " "))
        hot = random.randint(1, 6)
        name = self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dt > span.hot-search-item > span:nth-child({})".format(
                hot)).text
        print("商标名称:" + name)
        self.driver.find_element_by_css_selector(
            "body > div.section-banner > div.public-search > div > dl > dt > span.hot-search-item > span:nth-child({})".format(
                hot)).click()

        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        print(self.driver.title)
        dl.refresh()
        time.sleep(3)
        zf = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(zf))
        number = re.sub(r"\D", "", zf)
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0,1200)")  # 滑动滚动条
        if int(number) == 0:
            tips = self.driver.find_element_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > div.no-search-data > div").text
            print(str(tips).replace("\n", " "))
            print("热搜跳转正常,测试通过!")
        else:
            brand = self.driver.find_element_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > a > h2").text
            print("商标名称:" + brand)
            info = self.driver.find_element_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > div > ul").text
            print(str(info).replace("\n", " "))
            print("热搜跳转正常,测试通过!")

        get_screenshort(self.driver, "test_trademark_hot_2.png")

    def test_PreliminaryPublicationQuery(self):
        """初审公告查询测试"""

        dl = DengLuPage(self.driver)
        time.sleep(2)
        self.driver.get("https://so.quandashi.com/search/notice/index")
        dl.refresh()
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        self.assertIn("初审公告搜索", self.driver.title)
        print(self.driver.title)
        dl.refresh()
        brand1 = unicode()
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(1) > input[type=\"text\"]").send_keys(
            brand1)
        print("商标名称:" + brand1)
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(2) > label:nth-child(1) > span").click()
        lx1 = self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(2) > label:nth-child(1) > span").text
        print("搜索类型:" + str(lx1))
        time.sleep(2)
        get_screenshort(self.driver, "test.png")
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        js = "return document.getElementsByClassName(\"search-num\")[0].innerText;"
        ss = self.driver.execute_script(js)
        print(str(ss))

        time.sleep(2)
        get_screenshort(self.driver, "test_PreliminaryPublicationQuery_1.png")
        self.driver.refresh()

        brand2 = unicode()
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(1) > input[type=\"text\"]").send_keys(
            brand2)
        print("商标名称:" + brand2)
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(2) > label:nth-child(2)").click()
        lx2 = self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(2) > label:nth-child(2)").text
        print("搜索类型:" + lx2)
        time.sleep(2)
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        js = "return document.getElementsByClassName(\"search-num\")[0].innerText;"
        ss = self.driver.execute_script(js)
        print(str(ss))
        time.sleep(2)
        get_screenshort(self.driver, "test_PreliminaryPublicationQuery_2.png")
        self.driver.refresh()

        brand3 = unicode()
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(1) > input[type=\"text\"]").send_keys(
            brand3)
        print("商标名称:" + brand3)
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(2) > label:nth-child(3) > span").click()
        lx3 = self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(2) > label:nth-child(3) > span").text
        print("搜索类型:" + lx3)
        time.sleep(2)
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        js = "return document.getElementsByClassName(\"search-num\")[0].innerText;"
        ss = self.driver.execute_script(js)
        print(str(ss))
        time.sleep(2)
        get_screenshort(self.driver, "test_PreliminaryPublicationQuery_3.png")

    def test_PreliminaryPublicationExport(self):
        """初审公告导出测试"""
        dl = DengLuPage(self.driver)
        time.sleep(2)
        self.driver.get("https://so.quandashi.com/")
        time.sleep(2)
        self.driver.find_element_by_css_selector(
            "body > div.page > div.page-index > div.page-index-form.search > ul.page-index-icon > li:nth-child(1) > a > img").click()
        self.driver.set_window_size(1920, 1080)
        title_ls = list()
        title_ls.append(self.driver.title)
        self.assertIn("初审公告搜索", title_ls)
        print(self.driver.title)
        dl.refresh()
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(1) > input[type=\"text\"]").send_keys(
            "大王")
        print("商标名称:大王")
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        result = self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > span").text
        print(str(result))
        """点击导出数据"""
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > div > a.button.button-white").click()
        time.sleep(5)
        print("初审公告报告导出测试通过!请在默认目录查看文件!")

    def test_PreliminaryPublicationDetails(self):
        """初审公告详情测试"""
        dl = DengLuPage(self.driver)
        time.sleep(2)
        self.driver.get("https://so.quandashi.com/search/notice/index")
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        title_ls = list()
        title_ls.append(self.driver.title)
        self.assertIn("初审公告搜索", title_ls)
        print(self.driver.title)
        dl.refresh()
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(1) > input[type=\"text\"]").send_keys(
            "大")
        print("商标名称:大")
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        result = self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > span").text
        print(str(result))
        """查询到的第一个商标信息"""
        info = self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-content > table > tbody > tr:nth-child(3)").text
        print("商标信息:" + str(info).replace("\n", " ").replace("查看详情", "").replace("我要异议", ""))

        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-content > table > tbody > tr:nth-child(3) > td.td-href > a:nth-child(1)").click()
        # 获取打开的多个窗口句柄
        windows = self.driver.window_handles
        # 切换到当前最新打开的窗口
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        get_screenshort(self.driver, "test_PreliminaryPublicationDetails_1.png")
        """点击下载初审公告"""
        self.driver.find_element_by_css_selector(
            "body > div.page > div.w-center > div.page-detail > div.btns > a.sc_notice_download.button.button-white").click()
        time.sleep(5)
        print("初审公告pdf文件下载测试通过!请在默认目录查看文件!")
        self.driver.find_element_by_css_selector(
            "body > div.page > div.w-center > div.page-detail > div.btns > a.sc_notice_brand.button").click()
        time.sleep(2)
        get_screenshort(self.driver, "test_PreliminaryPublicationDetails_2.png")

    def test_PreliminaryPublicationBusiness(self):
        """我要异议测试"""
        dl = DengLuPage(self.driver)
        time.sleep(2)
        self.driver.get("https://so.quandashi.com/search/notice/index")
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        title_ls = list()
        title_ls.append(self.driver.title)
        self.assertIn("初审公告搜索", title_ls)
        print(self.driver.title)
        dl.refresh()

        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        """点击我要异议"""
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-content > table > tbody > tr:nth-child(3) > td.td-href > a.notice_business").click()
        get_screenshort(self.driver, "test_PreliminaryPublicationBusiness.png")
        print("初审公告异议测试通过!")

    def test_PreliminaryPublicationConditions(self):
        """初审公告筛选条件测试"""
        dl = DengLuPage(self.driver)
        time.sleep(2)
        self.driver.get("https://so.quandashi.com/search/notice/index")
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        title_ls = list()
        title_ls.append(self.driver.title)
        self.assertIn("初审公告搜索", title_ls)
        print(self.driver.title)
        dl.refresh()
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(1) > li:nth-child(1) > input[type=\"text\"]").send_keys(
            "大王")
        print("商标名称:大王")
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > a").click()
        time.sleep(5)
        result_1 = self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > span").text
        print(str(result_1))
        sl_1 = int(re.sub(r"\D", "", str(result_1)))

        """筛选条件"""
        self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > ul:nth-child(2) > li > a").click()
        number = random.randint(1, 45)
        lb = self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(2) > li > div.category-show-box.select-show-category > a:nth-child({})".format(
                number)).text
        self.driver.find_element_by_css_selector(
            "#noticeList > div > div.page-form > ul:nth-child(2) > li > div.category-show-box.select-show-category > a:nth-child({})".format(
                number)).click()
        print("选择申请类别:" + lb)
        time.sleep(5)

        result_2 = self.driver.find_element_by_css_selector("#noticeList > div > div.page-form > div > span").text
        print(str(result_2))
        sl_2 = int(re.sub(r"\D", "", result_2))

        if sl_1 > sl_2:
            print("初审公告筛选申请类别测试通过!")
        else:
            self.assertEqual(sl_1, sl_2, "筛选条件异常请及时查看!")

    def test_patent_search(self):
        """专利搜索测试"""
        dl = DengLuPage(self.driver)
        dl.login()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#qds-search-common > li:nth-child(2)").click()

        patent = ["摩托车", "自行车", "电动车", "ofo"]

        zl = random.choice(patent)
        self.driver.find_element_by_css_selector("#qds-searchkey").send_keys(zl)
        print("专利名称:" + str(zl))
        self.driver.find_element_by_css_selector("#serch-word").click()
        # 获取打开的多个窗口句柄
        windows = self.driver.window_handles
        # 切换到当前最新打开的窗口
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        self.driver.set_window_size(1920, 1080)
        dl.refresh()
        time.sleep(5)
        self.assertIn("注册专利查询_中国专利查询系统_让知识产生财富_权大师", self.driver.title)
        print(self.driver.title)
        num = self.driver.find_element_by_css_selector(
            "body > div.patentSearchList-wrap.searchList-wrap > div.sort-condition.songti > div > div.s-left > dl > dt").text

        get_screenshort(self.driver, "test_patent_search.png")
        print(str(num))
        number = re.sub(r"\D", "", num)

        if int(number) == 0:
            self.assertEqual(1, 0, "专利搜索异常!")
        else:
            pass

        print(number)

        print("专利搜索测试通过!")

    def test_enterprise_search(self):
        """企业搜索测试"""
        dl = DengLuPage(self.driver)
        dl.login()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#qds-search-common > li:nth-child(3)").click()
        company = unicode()
        self.driver.find_element_by_css_selector("#qds-searchkey").send_keys(company)
        print(str(company))
        self.driver.find_element_by_css_selector("#serch-word").click()
        # 获取打开的多个窗口句柄
        windows = self.driver.window_handles
        # 切换到当前最新打开的窗口
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        # self.assertIn("注册专利查询_中国专利查询系统_让知识产生财富_权大师", self.driver.title)
        print(self.driver.title)
        print(self.driver.current_url)

    def test_cross(self):
        """交叉检索测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        time.sleep(2)
        mark = ("小米", unicode())
        brand = random.choice(mark)
        self.driver.find_element_by_name("key").send_keys(brand)
        print("搜索商标:" + brand)
        self.driver.find_element_by_id("btnSearchkey").click()
        time.sleep(3)

        # html = self.driver.execute_script("return document.documentElement.outerHTML")
        # print(str(html))

        """交叉检索"""
        self.driver.find_element_by_class_name("cross-search").click()
        classify = random.randint(1, 45)
        time.sleep(2)

        dl = self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > li:nth-child({})".format(classify)).text
        print(str(dl))
        self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > li:nth-child({})".format(classify)).click()
        time.sleep(2)

        zl = self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > li.list.open > div:nth-child(2) > span").text
        print(str(zl))
        self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > li.list.open > div:nth-child(2) > span").click()
        time.sleep(2)

        xl = self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > li.list.open > div.title-second.open > dl > dt:nth-child(1) > span").text
        print(str(xl))
        self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > li.list.open > div.title-second.open > dl > dt:nth-child(1) > span").click()
        time.sleep(2)

        # ol = self.driver.find_element_by_css_selector("#section-selfchoice > div.group-left > ul > li.list.open > div.title-second.open > dl > dt:nth-child(1) > span").text
        # print(str(ol))
        # self.driver.find_element_by_css_selector("#section-selfchoice > div.group-left > ul > li.list.open > div.title-second.open > dl > dt:nth-child(1) > span").click()

        info = self.driver.find_element_by_class_name("cross-range-list").text
        print(str(info).replace("\n", " "))

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.w_category_modal > div > div.btns > a").click()
        time.sleep(2)
        """已选条件"""

        select = self.driver.find_element_by_class_name("selected-category").text
        print((str(select).replace("\n", " ")).replace("×", " "))

        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top > i").text
        print("权大师为您找到相关结果{}个".format(result))
        time.sleep(2)
        if int(result) == 0:
            print("亲，未检测到您关注的商标，请换个词试试~ 不过您可以就~{}~提起商标申请哦".format(brand))
        else:
            # 第一个商标信息
            jg1 = self.driver.find_element_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > div > ul").text
            print(str(jg1).replace("\n", " "))
        get_screenshort(self.driver, "test_cross.png")

    def test_hot_trade(self):
        """热门商标出售测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        time.sleep(2)
        self.driver.find_element_by_name("key").send_keys("小米")
        self.driver.find_element_by_id("btnSearchkey").click()
        time.sleep(5)

        trade = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-right > div > ul > li:nth-child(1) > div.hot-brand-detail").text
        print("热门商标信息:" + str(trade).replace("\n", " "))

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-right > div > ul > li:nth-child(1) > div.hot-brand-detail > a").click()
        get_screenshort(self.driver, "test_hot_trade.png")
        print("热门商标信息正常测试通过!")

    def test_try(self):
        """尝试注册测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        time.sleep(2)
        brand = unicode()
        self.driver.find_element_by_name("key").send_keys(brand)
        self.driver.find_element_by_id("btnSearchkey").click()
        time.sleep(3)

        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top > i").text
        print(result)
        time.sleep(2)

        if int(result) == 0:
            print("亲，未检测到您关注的商标，请换个词试试~ 不过您可以就~{}~提起商标申请哦".format(brand))

            wsq = self.driver.find_element_by_css_selector(
                "#searchList > div.page-form.w-center > div.no-result-category > div.no-result-category-box > a:nth-child(1)").text
            print(str(wsq))
            self.driver.find_element_by_css_selector(
                "#searchList > div.page-form.w-center > div.no-result-category > div.no-result-category-box > a:nth-child(1)").click()

            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            time.sleep(2)
            self.driver.set_window_size(1920, 1080)
            print(self.driver.current_url)
            get_screenshort(self.driver, "test_try.png")

        else:
            # 搜索结果
            jg = self.driver.find_element_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
            print(jg)

            # 第一个商标信息
            jg1 = self.driver.find_element_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > div > ul").text
            print(str(jg1).replace("\n", " "))

    def test_geography(self):

        """地理标志商标测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        self.driver.find_element_by_name("key").send_keys(xz("phLocaltionTM.txt").replace(".0", ""))
        time.sleep(2)
        self.driver.find_element_by_css_selector(
            "body > div.page > div.page-index > div.page-index-form.search > ul.page-index-icon > li:nth-child(4) > a > img").click()
        time.sleep(5)

        selected = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category").text
        print((str(selected).replace("\n", " ")).replace("×", " "))
        selected_1 = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category > div.selected-category-box > a:nth-child(1) > span").text
        if selected_1 == "地理标志":
            pass
        else:
            self.assertEqual(1, 2, "已选条件异常请及时查看")

        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        number = 1
        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child({}) > div.result-href".format(
                number)).text
        print(str(info).replace("\n", " "))

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child({}) > div.result-href".format(
                number)).click()

        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        print(self.driver.current_url)

        result2 = self.driver.find_element_by_css_selector(
            "#searchDetail > div.page-brand > div > div.brand-left > div.brand-info > h2").text
        get_screenshort(self.driver, "test_geography.png")
        print(str(result2))

    def test_famous(self):

        """驰著名商标测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        self.driver.find_element_by_name("key").send_keys(xz("famousTM_2.txt").replace(".0", ""))
        time.sleep(2)
        self.driver.find_element_by_css_selector(
            "body > div.page > div.page-index > div.page-index-form.search > ul.page-index-icon > li:nth-child(3) > a > img").click()
        time.sleep(5)

        selected = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category").text
        print((str(selected).replace("\n", " ")).replace("×", " "))

        selected_1 = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category > div.selected-category-box > a:nth-child(1) > span").text
        if selected_1 == "驰名商标":
            pass
        else:
            self.assertEqual(1, 2, "已选条件异常请及时查看")

        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        number = 1
        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child({}) > div.result-href".format(
                number)).text
        print(str(info).replace("\n", " "))

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child({}) > div.result-href".format(
                number)).click()

        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        print(self.driver.current_url)
        get_screenshort(self.driver, "test_famous.png")
        result2 = self.driver.find_element_by_css_selector(
            "#searchDetail > div.page-brand > div > div.brand-left > div.brand-info > h2").text
        print(str(result2))

    def test_special_trademark(self):

        """特殊商标测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        time.sleep(2)

        trademark = ("phLocaltionTM.txt", "famousTrandMark.txt", "famousTM_1.txt")
        filename = random.choice(trademark)
        print(filename)
        application_number = xz(filename)
        print("申请号:" + str(application_number).replace(".0", ""))

        self.driver.find_element_by_css_selector(
            "body > div.page > div.page-index > div.page-index-form.search > div > input.input.search-text").send_keys(
            str(application_number).replace(".0", ""))
        self.driver.find_element_by_css_selector("#btnSearchkey").click()
        time.sleep(5)

        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href").text
        print(str(info).replace("\n", " "))
        number = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li > div.result-href > div.brand-info > div > ul > li:nth-child(2) > span:nth-child(4)").text
        print(str(number))

        self.assertIn(str(application_number).replace(".0", ""), str(number))

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href").click()

        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)
        print(self.driver.current_url)

        result2 = self.driver.find_element_by_css_selector(
            "#searchDetail > div.page-brand > div > div.brand-left > div.brand-info > h2").text
        get_screenshort(self.driver, "test_special_trademark.png")
        print(str(result2))

    def test_special_search(self):

        """特殊搜索测试"""
        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/")
        dl.refresh()
        time.sleep(2)
        self.driver.find_element_by_css_selector(
            "body > div.page > div.page-index > div.page-index-form.search > div > input.input.search-text").send_keys(
            xz("famousTM_3.txt").replace(".0", ""))
        self.driver.find_element_by_css_selector("#btnSearchkey").click()
        time.sleep(5)

        # """删除搜索商标"""
        # self.driver.find_element_by_css_selector("#searchList > div.page-search.w-center > div.search-input > input").send_keys(Keys.BACK_SPACE)
        # time.sleep(2)
        """点击驰名商标"""

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > ul > li:nth-child(4) > div.category-show-box > a:nth-child(2)").click()
        time.sleep(5)
        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href").text
        print(str(info).replace("\n", " "))

        for link in self.driver.find_elements_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > a"):
            print(link.get_attribute("href"))

        selected = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category").text
        print((str(selected).replace("\n", " ")).replace("×", " "))

        """点击著名商标"""

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > ul > li:nth-child(4) > div.category-show-box > a:nth-child(3)").click()
        time.sleep(5)
        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href").text
        print(str(info).replace("\n", " "))

        for link in self.driver.find_elements_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > a"):
            print(link.get_attribute("href"))

        selected = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category").text
        print((str(selected).replace("\n", " ")).replace("×", " "))

        """点击地理标志商标"""

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > ul > li:nth-child(4) > div.category-show-box > a:nth-child(4)").click()
        time.sleep(5)
        result = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > div.search-top").text
        print(str(result))

        info = self.driver.find_element_by_css_selector(
            "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href").text
        print(str(info).replace("\n", " "))

        for link in self.driver.find_elements_by_css_selector(
                "#searchList > div.page-content.w-center > div.page-content-left > ul > li:nth-child(1) > div.result-href > div.brand-info > a"):
            print(link.get_attribute("href"))

        selected = self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > div.selected-category").text
        print((str(selected).replace("\n", " ")).replace("×", " "))

    def test_nice_search(self):
        """尼斯分类搜索(search)"""

        dl = DengLuPage(self.driver)
        self.driver.get("https://so.quandashi.com/index/search?key=%E6%91%A9%E6%89%98%E8%BD%A6")
        dl.refresh()

        self.driver.find_element_by_css_selector(
            "#searchList > div.page-form.w-center > ul > li:nth-child(4) > div.category-show-box > a.cross-search").click()

        self.driver.find_element_by_css_selector("#section-selfchoice > div.group-left > div > div > input").send_keys(
            "摩托车")
        self.driver.find_element_by_css_selector("#btn-search > i").click()
        time.sleep(3)

        number_1 = self.driver.find_element_by_css_selector(
            "#section-selfchoice > div.group-left > ul > div > li:nth-child(1) > span").text

        number_2 = re.sub(r"\D", "", number_1)

        number_3 = int(number_2) + 0

        self.assertEqual(number_3, 7, "尼斯分类搜索结果异常!")

        print("so.QDS.com商标注册尼斯分类搜索结果正常!")
