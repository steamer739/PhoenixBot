from theming.styles import globalStyles
from PyQt5 import QtCore, QtGui, QtWidgets
from utils import return_data,write_data,Encryption,search_newegg
import sys,platform,settings

def no_abort(a, b, c):
    sys.__excepthook__(a, b, c)
sys.excepthook = no_abort

class SearchPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SearchPage, self).__init__(parent)
        self.header_font = self.create_font("Arial", 18)
        self.small_font = self.create_font("Arial", 13)
        self.setupUi(self)
        self.load_tasks()
      

    def create_font(self, family, pt_size) -> QtGui.QFont:
        font = QtGui.QFont()
        font.setPointSize(pt_size) if platform.system() == "Darwin" else font.setPointSize(pt_size * .75)
        font.setFamily(family)
        font.setWeight(50)
        return font

    def create_header(self, parent, rect, font, text) -> QtWidgets.QLabel:
        header = QtWidgets.QLabel(self.search_card)
        header.setParent(parent)
        header.setGeometry(rect)
        header.setFont(font)
        header.setStyleSheet("color: rgb(212, 214, 214);border: none;")
        header.setText(text)
        return header

    def create_checkbox(self, rect, text) -> QtWidgets.QCheckBox:
        checkbox = QtWidgets.QCheckBox(self.search)
        checkbox.setGeometry(rect)
        checkbox.setStyleSheet("color: #FFFFFF;border: none;")
        checkbox.setText(text)
        return checkbox

    def create_edit(self, parent, rect, font, placeholder) -> QtWidgets.QLineEdit:
        edit = QtWidgets.QLineEdit(parent)
        edit.setGeometry(rect)
        edit.setStyleSheet("outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        edit.setFont(font)
        edit.setPlaceholderText(placeholder)
        edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        return edit

    def setupUi(self, searchpage):
        global tasks
        self.tasks = []
        tasks = self.tasks
        self.searchpage = searchpage
        font = QtGui.QFont()
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13*.75)
        font.setFamily("Arial")
        self.searchpage.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.searchpage.setGeometry(QtCore.QRect(60, 0, 1041, 601))
        self.searchpage.setStyleSheet("QComboBox::drop-down {    border: 0px;}QComboBox::down-arrow {    image: url(images/down_icon.png);    width: 14px;    height: 14px;}QComboBox{    padding: 1px 0px 1px 3px;}QLineEdit:focus {   border: none;   outline: none;}")
        self.search_card = QtWidgets.QWidget(self.searchpage)
        self.search_card.setGeometry(QtCore.QRect(30, 45, 991, 51))
        self.search_card.setStyleSheet("background-color: {};border-radius: 10px;border: 1px solid #2e2d2d;".format(globalStyles["backgroundLight"]))
        self.search_label = QtWidgets.QLabel(self.search_card)
        self.search_label.setGeometry(QtCore.QRect(80, 10, 91, 31))
        self.search_label.setFont(font)
        self.search_label.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.search_label.setText("Total Tasks")
        self.search_btn = QtWidgets.QPushButton(self.search_card)
        self.search_btn.setGeometry(QtCore.QRect(400, 10, 86, 32))
        self.search_btn.setFont(self.small_font)
        self.search_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_btn.setStyleSheet("color: #FFFFFF;background-color: {};border-radius: 10px;border: 1px solid #2e2d2d;".format(globalStyles["primary"]))
        self.search_btn.setText("Search")
        self.search_btn.clicked.connect(self.search_item)
        self.loadlist_box = QtWidgets.QComboBox(self.searchpage)
        self.loadlist_box.setGeometry(QtCore.QRect(540, 60, 161, 21))
        self.loadlist_box.setFont(font)
        self.loadlist_box.setStyleSheet("color: #FFFFFF;background-color: {};border-radius: 10px;border: 1px solid #2e2d2d;".format(globalStyles["primary"]))
        self.loadlist_box.addItem("Website")
        self.loadlist_box.addItem("All")
        self.loadlist_box.addItem("Newegg")
        self.loadlist_box.addItem("Bestbuy")
        self.loadlist_box.addItem("Target")
        self.loadlist_box.addItem("Walmart")
        self.loadlist_box.currentTextChanged.connect(self.search_item)
        self.proxies_header = self.create_header(self.searchpage, QtCore.QRect(30, 10, 150, 31),self.create_font("Arial", 22), "Item Lookup")
        
        #Search result section
        self.search_card = QtWidgets.QWidget(self.searchpage)
        self.search_card.setGeometry(QtCore.QRect(30, 110, 991, 461))
        self.search_card.setStyleSheet("background-color: {};border-radius: 20px;border: 1px solid #2e2d2d;".format(globalStyles["backgroundLight"]))
        self.scrollArea = QtWidgets.QScrollArea(self.search_card)
        self.scrollArea.setGeometry(QtCore.QRect(20, 30, 951, 421))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet("border:none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 951, 421))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setSpacing(2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.image_table_header = QtWidgets.QLabel(self.search_card)
        self.image_table_header.setGeometry(QtCore.QRect(40, 7, 51, 31))
        self.image_table_header.setText("Image")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15) if platform.system() == "Darwin" else font.setPointSize(15*.75)
        font.setBold(False)
        font.setWeight(50)
        self.image_table_header.setFont(font)
        self.image_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.product_table_header = QtWidgets.QLabel(self.search_card)
        self.product_table_header.setGeometry(QtCore.QRect(240, 7, 61, 31))
        self.product_table_header.setFont(font)
        self.product_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.product_table_header.setText("Link")
        self.type_table_header = QtWidgets.QLabel(self.search_card)
        self.type_table_header.setGeometry(QtCore.QRect(590, 7, 61, 31))
        self.type_table_header.setFont(font)
        self.type_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.type_table_header.setText("Type")
        self.profile_table_header = QtWidgets.QLabel(self.search_card)
        self.profile_table_header.setGeometry(QtCore.QRect(650, 7, 61, 31))
        self.profile_table_header.setFont(font)
        self.profile_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.profile_table_header.setText("Profile")
        self.status_table_header = QtWidgets.QLabel(self.search_card)
        self.status_table_header.setGeometry(QtCore.QRect(710, 7, 61, 31))
        self.status_table_header.setFont(font)
        self.status_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.status_table_header.setText("Status")
        self.actions_table_header = QtWidgets.QLabel(self.search_card)
        self.actions_table_header.setGeometry(QtCore.QRect(890, 7, 61, 31))
        self.actions_table_header.setFont(font)
        self.actions_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.actions_table_header.setText("Actions")
        self.site_table_header = QtWidgets.QLabel(self.search_card)
        self.site_table_header.setGeometry(QtCore.QRect(160, 7, 61, 31))
        self.site_table_header.setFont(font)
        self.site_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.site_table_header.setText("Site")
        self.id_header = QtWidgets.QLabel(self.search_card)
        self.id_header.setGeometry(QtCore.QRect(110, 7, 31, 31))
        self.id_header.setFont(font)
        self.id_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.id_header.setText("ID")
        self.set_data()
        QtCore.QMetaObject.connectSlotsByName(searchpage)

    
    def load_tasks(self):
        tasks_data = return_data("./data/tasks.json")
        write_data("./data/tasks.json",[])
        try:
            for task in tasks_data:
                tab = SearchTab(task["site"],task["product"],task["profile"],task["proxies"],task["monitor_delay"],task["error_delay"],task["max_price"],self.stop_all_tasks,self.scrollAreaWidgetContents)
                self.verticalLayout.takeAt(self.verticalLayout.count()-1)
                self.verticalLayout.addWidget(tab)
                spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.verticalLayout.addItem(spacerItem)
        except:
            pass

    def search_item(self):
        items = search_newegg.get_items()
        for item in items:
            print(item['link'])
            SearchTab(item['link'])


    def set_data(self):
        settings = return_data("./data/settings.json")
        self.update_settings(settings)

    def save_settings(self):
        settings = {"webhook":            self.webhook_edit.text(),
                    "webhookonbrowser":   self.browser_checkbox.isChecked(),
                    "webhookonorder":     self.order_checkbox.isChecked(),
                    "webhookonfailed":    self.paymentfailed_checkbox.isChecked(),
                    "browseronfailed":    self.onfailed_checkbox.isChecked(),
                    "onlybuyone":         self.buy_one_checkbox.isChecked(),
                    "dont_buy":           self.dont_buy_checkbox.isChecked(),
                    "random_delay_start": self.random_delay_start.text(),
                    "random_delay_stop":  self.random_delay_stop.text(),
                    "bestbuy_user": self.bestbuy_user_edit.text(),
                    "bestbuy_pass": Encryption().encrypt(self.bestbuy_pass_edit.text()).decode("utf-8"),
                    "target_user": self.target_user_edit.text(),
                    "target_pass": Encryption().encrypt(self.target_pass_edit.text()).decode("utf-8"),
                    "gamestop_user": self.gamestop_user_edit.text(),
                    "gamestop_pass": Encryption().encrypt(self.gamestop_pass_edit.text()).decode("utf-8")}

        write_data("./data/settings.json",settings)
        self.update_settings(settings)
        QtWidgets.QMessageBox.information(self, "Phoenix Bot", "Saved Settings")

    def update_settings(self, settings_data):
        global webhook, webhook_on_browser, webhook_on_order, webhook_on_failed, browser_on_failed, dont_buy, random_delay_start, random_delay_stop, target_user, target_pass, gamestop_user, gamestop_pass
        settings.webhook, settings.webhook_on_browser, settings.webhook_on_order, settings.webhook_on_failed, settings.browser_on_failed, settings.buy_one, settings.dont_buy = settings_data["webhook"], settings_data["webhookonbrowser"], settings_data["webhookonorder"], settings_data["webhookonfailed"], settings_data["browseronfailed"], settings_data['onlybuyone'], settings_data['dont_buy']

        if settings_data.get("random_delay_start", "") != "":
            settings.random_delay_start = settings_data["random_delay_start"]
        if settings_data.get("random_delay_stop", "") != "":
            settings.random_delay_stop = settings_data["random_delay_stop"]
        if settings_data.get("bestbuy_user", "") != "":
            settings.bestbuy_user = settings_data["bestbuy_user"]
        if settings_data.get("bestbuy_pass", "") != "":
            settings.bestbuy_pass = (Encryption().decrypt(settings_data["bestbuy_pass"].encode("utf-8"))).decode("utf-8")
        if settings_data.get("target_user", "") != "":
            settings.target_user = settings_data["target_user"]
        if settings_data.get("target_pass", "") != "":
            settings.target_pass = (Encryption().decrypt(settings_data["target_pass"].encode("utf-8"))).decode("utf-8")
        if settings_data.get("gamestop_user", "") != "":
            settings.gamestop_user = settings_data["gamestop_user"]
        if settings_data.get("gamestop_pass", "") != "":
            settings.gamestop_pass = (Encryption().decrypt(settings_data["gamestop_pass"].encode("utf-8"))).decode("utf-8")

class SearchTab(QtWidgets.QWidget):
    def __init__(self,product,parent=None):
        super(SearchTab, self).__init__(parent)
        self.product
        self.setupUi(self)

    def setupUi(self,SearchTab):
        self.running = False
        self.SearchTab = SearchTab
        self.SearchTab.setMinimumSize(QtCore.QSize(0, 50))
        self.SearchTab.setMaximumSize(QtCore.QSize(16777215, 50))
        self.SearchTab.setStyleSheet("border-radius: none;")
        self.product_label = QtWidgets.QLabel(self.SearchTab)
        self.product_label.setGeometry(QtCore.QRect(222, 10, 250, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13*.75)
        font.setBold(False)
        font.setWeight(50)
        self.product_label.setFont(font)
        self.product_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.profile_label = QtWidgets.QLabel(self.SearchTab)
        self.profile_label.setGeometry(QtCore.QRect(650, 10, 51, 31))
        self.profile_label.setFont(font)
        self.profile_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.status_label = QtWidgets.QLabel(self.SearchTab)
        self.status_label.setGeometry(QtCore.QRect(710, 10, 231, 31))
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.browser_label = QtWidgets.QLabel(self.SearchTab)
        self.browser_label.setGeometry(QtCore.QRect(632, 10, 231, 31))
        self.browser_label.setFont(font)
        self.browser_label.setStyleSheet("color: rgb(163, 149, 255);")
        self.browser_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browser_label.mousePressEvent = self.open_browser
        self.browser_label.hide()
        self.start_btn = QtWidgets.QLabel(self.SearchTab)
        self.start_btn.setGeometry(QtCore.QRect(870, 15, 16, 16))
        self.start_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_btn.setPixmap(QtGui.QPixmap("images/play.png"))
        self.start_btn.setScaledContents(True)
        self.start_btn.mousePressEvent = self.start
        self.stop_btn = QtWidgets.QLabel(self.SearchTab)
        self.stop_btn.setGeometry(QtCore.QRect(870, 15, 16, 16))
        self.stop_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stop_btn.setPixmap(QtGui.QPixmap("images/stop.png"))
        self.stop_btn.setScaledContents(True)
        self.stop_btn.mousePressEvent = self.stop
        self.delete_btn = QtWidgets.QLabel(self.SearchTab)
        self.delete_btn.setGeometry(QtCore.QRect(920, 15, 16, 16))
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_btn.setPixmap(QtGui.QPixmap("images/trash.png"))
        self.delete_btn.setScaledContents(True)
        self.delete_btn.mousePressEvent = self.delete
        self.edit_btn = QtWidgets.QLabel(self.SearchTab)
        self.edit_btn.setGeometry(QtCore.QRect(895, 15, 16, 16))
        self.edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_btn.setPixmap(QtGui.QPixmap("images/edit.png"))
        self.edit_btn.setScaledContents(True)
        self.edit_btn.mousePressEvent = self.edit
        self.image = QtWidgets.QLabel(self.SearchTab)
        self.image.setGeometry(QtCore.QRect(20, 0, 50, 50))
        self.image.setPixmap(QtGui.QPixmap("images/no_image.png"))
        self.image.setScaledContents(True)
        self.site_label = QtWidgets.QLabel(self.SearchTab)
        self.site_label.setGeometry(QtCore.QRect(140, 10, 61, 31))
        self.site_label.setFont(font)
        self.site_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.id_label = QtWidgets.QLabel(self.SearchTab)
        self.id_label.setGeometry(QtCore.QRect(90, 10, 31, 31))
        self.id_label.setFont(font)
        self.id_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.stop_btn.raise_()
        self.product_label.raise_()
        self.profile_label.raise_()
        self.browser_label.raise_()
        self.start_btn.raise_()
        self.delete_btn.raise_()
        self.image.raise_()
        self.site_label.raise_()
        self.monitor_delay_label = QtWidgets.QLabel(self.SearchTab)
        self.monitor_delay_label.hide()
        self.error_delay_label = QtWidgets.QLabel(self.SearchTab)
        self.error_delay_label.hide()
        self.max_price_label = QtWidgets.QLabel(self.SearchTab)
        self.max_price_label.hide()
        self.proxies_label = QtWidgets.QLabel(self.SearchTab)
        self.proxies_label.hide()
        self.load_labels()


    def load_labels(self):
        self.id_label.setText(self.task_id)
        self.product_label.setText(self.product)
        self.profile_label.setText(self.profile)
        self.proxies_label.setText(self.proxies)
        self.status_label.setText("Idle")
        self.browser_label.setText("Click To Open Browser")
        self.site_label.setText(self.site)
        self.monitor_delay_label.setText(self.monitor_delay)
        self.error_delay_label.setText(self.error_delay)
        self.max_price_label.setText(self.max_price)

    