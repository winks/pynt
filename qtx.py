from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl, QMargins
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
  def __init__(self, pynt):
    self.pynt = pynt
    self.bootstrap()

  def bootstrap(self):
    self.no_margin = QMargins(0, 0, 0, 0)
    self.app = App()

    self.scroll_area = QScrollArea()
    self.scroll_area.setContentsMargins(self.no_margin)
    self.scroll_area.setBackgroundRole(QPalette.Dark);
    self.scroll_area.setWidgetResizable(True)

    self.main_layout = QVBoxLayout()
    self.main_layout.setSpacing(0)
    self.main_layout.setContentsMargins(self.no_margin)
    self.main_layout.addWidget(self.scroll_area)

    self.contents = QWidget()
    self.contents.setWindowTitle("Pynt")
    self.contents.setContentsMargins(self.no_margin)
    self.contents.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    #self.contents.setScaledContents(True)

    self.scroll_area.setWidget(self.contents)

    self.layout = QVBoxLayout(self.contents)
    self.layout.setSizeConstraint(QLayout.SetMinimumSize)

    return self

  def addStuff(self, posts):
    for post in posts:
      panel_layout = QVBoxLayout()
      panel_layout.setSpacing(0)
      panel_layout.setContentsMargins(self.no_margin)

      panel = QFrame()
      panel.setLayout(panel_layout)
      panel.setContentsMargins(self.no_margin)
      panel.setStyleSheet("background-color:green;")

      control_layout = QHBoxLayout()
      control_layout.setSpacing(0)
      control_layout.setContentsMargins(self.no_margin)

      controls = QFrame()
      controls.setStyleSheet("background-color:#ffeeee;")
      controls.setContentsMargins(self.no_margin)
      controls.setLayout(control_layout)

      btn_url = QPushButton()
      btn_url.setContentsMargins(self.no_margin)
      btn_url.setStyleSheet("QPushButton { color: black; }")
      btn_url.setFlat(True)

      label = QPushButton()
      label.setContentsMargins(self.no_margin)
      label.setStyleSheet("color:#000000;")
      label.setFlat(True)

      btn_user = QPushButton()
      btn_user.setContentsMargins(self.no_margin)
      btn_user.setStyleSheet("QPushButton { color: black; }")
      btn_user.setFlat(True)

      view = WebView()
      #view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
      view.setMinimumHeight(200)
      view.setContentsMargins(self.no_margin)
      view.setStyleSheet("background-color:#eeeeff;")

      control_layout.addWidget(btn_user)
      control_layout.addWidget(label)
      control_layout.addWidget(btn_url)

      panel_layout.addWidget(controls)
      panel_layout.addWidget(view)

      self.layout.addWidget(panel)

      # finally, set the data to the widgets
      domain = post["guid"].split('/')[0]

      btn_url.setText(post["url"])
      label.setText(post["edited_at"])
      btn_user.setText(self.pynt.users[domain]["display_name"])
      view.setHtml(post["body_html"])

    return self

  def run(self):
    self.scroll_area.show()
    return self.app.exec_()
