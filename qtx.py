import ctypes
import platform

from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl, QMargins, Qt
from PyQt4.QtWebKit import QWebView, QWebPage

class WebView(QWebView):
  def __init__(self):
    QWebView.__init__(self)
    #self.loadFinished.connect(self._result_available)

  def _result_available(self, ok):
    frame = self.page().mainFrame()
    print unicode(frame.toHtml()).encode('utf-8')

class App(QApplication):
  def __init__(self):
    super(App, self).__init__([])

class PyntGui(object):
  pynt = None
  AVATAR_SIZE = 60
  AVATAR_DEFAULT = 'assets/example.org_user.jpg'
  WINDOW_TITLE = 'Pynt, for #pants'
  ICON_APP = 'assets/icons/pynt.png'
  ICON_USER = 'assets/icons/rainbow.png'
  ICON_TIME = 'assets/icons/time.png'
  ICON_URL = 'assets/icons/connect.png'

  def __init__(self, pynt):
    self.pynt = pynt
    self.bootstrap()

  def bootstrap(self):
    self.no_margin = QMargins(0, 0, 0, 0)
    self.app = App()
    self.app.setWindowIcon(QIcon(self.ICON_APP))
    if platform.system() == 'Windows':
      myappid = 'f5n.pynt.alpha'
      ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    self.scroll_area = QScrollArea()
    self.scroll_area.setContentsMargins(self.no_margin)
    self.scroll_area.setBackgroundRole(QPalette.Dark);
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWindowTitle(self.WINDOW_TITLE)

    self.main_layout = QVBoxLayout()
    self.main_layout.setSpacing(0)
    self.main_layout.setContentsMargins(self.no_margin)
    self.main_layout.addWidget(self.scroll_area)

    self.contents = QWidget()
    self.contents.setContentsMargins(self.no_margin)
    self.contents.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    #self.contents.setScaledContents(True)

    self.scroll_area.setWidget(self.contents)

    self.layout = QVBoxLayout(self.contents)
    self.layout.setSizeConstraint(QLayout.SetMinimumSize)

    return self

  def addStuff(self, posts):
    for post in posts:
      # xpanel holds one post
      xpanel_layout = QHBoxLayout()
      xpanel_layout.setSpacing(5)
      xpanel_layout.setContentsMargins(self.no_margin)

      xpanel = QFrame()
      xpanel.setContentsMargins(self.no_margin)
      xpanel.setLayout(xpanel_layout)

      avatar_label = self.updated_avatar(self.AVATAR_DEFAULT)

      # panel holds controls and view
      panel_layout = QVBoxLayout()
      panel_layout.setSpacing(0)
      panel_layout.setContentsMargins(self.no_margin)

      panel = QFrame()
      panel.setLayout(panel_layout)
      panel.setContentsMargins(self.no_margin)
      panel.setStyleSheet("background-color:green;")

      # control holds the controls at the top
      control_layout = QHBoxLayout()
      control_layout.setSpacing(0)
      control_layout.setContentsMargins(self.no_margin)

      controls = QFrame()
      controls.setStyleSheet("background-color:#ffeeee;")
      controls.setContentsMargins(self.no_margin)
      controls.setLayout(control_layout)

      # ctrl_ is inside control
      ctrl_url = QPushButton()
      ctrl_url.setContentsMargins(self.no_margin)
      ctrl_url.setStyleSheet("QPushButton { color: black; }")
      ctrl_url.setFlat(True)
      ctrl_url.setIcon(QIcon(self.ICON_URL))

      ctrl_updated = QPushButton()
      ctrl_updated.setContentsMargins(self.no_margin)
      ctrl_updated.setStyleSheet("color:#000000;")
      ctrl_updated.setFlat(True)
      ctrl_updated.setIcon(QIcon(self.ICON_TIME))

      ctrl_user = QPushButton()
      ctrl_user.setContentsMargins(self.no_margin)
      ctrl_user.setStyleSheet("QPushButton { color: black; }")
      ctrl_user.setFlat(True)
      ctrl_user.setIcon(QIcon(self.ICON_USER))

      # view displays HTML
      view = WebView()
      #view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
      view.setMinimumHeight(200)
      view.setContentsMargins(self.no_margin)
      view.setStyleSheet("background-color:#eeeeff;")


      # set the data to the widgets
      domain = post["guid"].split('/')[0]
      path = "assets/{}_user.jpg".format(domain)
      avatar_label = self.updated_avatar(path)

      ctrl_url.setText(post["url"])
      ctrl_updated.setText(post["edited_at"])
      ctrl_user.setText(self.pynt.users[domain]["display_name"])
      view.setHtml(post["body_html"])

      # now put everything together
      control_layout.addWidget(ctrl_user)
      control_layout.addWidget(ctrl_updated)
      control_layout.addWidget(ctrl_url)

      panel_layout.addWidget(controls)
      panel_layout.addWidget(view)

      xpanel_layout.addWidget(avatar_label, 0, Qt.AlignTop)
      xpanel_layout.addWidget(panel)

      self.layout.addWidget(xpanel)

    return self

  def updated_avatar(self, path):
    pixmap = QPixmap(path).scaled(self.AVATAR_SIZE,
                                  self.AVATAR_SIZE)
    image_label = QLabel()
    image_label.setPixmap(pixmap)

    return image_label

  def run(self):
    self.scroll_area.show()
    return self.app.exec_()
