import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QTextBrowser,
    QDesktopWidget,
)
from prediction import predict_arima
from utils import load_data, save_results
from plot import plot_predictions


class PredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """设置用户界面"""
        self.setWindowTitle("燃气使用预测-ARIMA")
        self.resize(800, 600)  # 将窗口大小设置为 800x600
        self.center()  # 调用自定义的居中函数

        layout = QVBoxLayout()

        # 选择数据文件按钮
        self.loadButton = QPushButton("选择数据文件", self)
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)

        # 显示当前选择的文件路径
        self.fileLabel = QLabel("未选择数据文件", self)
        layout.addWidget(self.fileLabel)

        # 运行预测按钮
        self.predictButton = QPushButton("开始预测", self)
        self.predictButton.clicked.connect(self.predictData)
        layout.addWidget(self.predictButton)

        # 导出结果按钮
        self.exportButton = QPushButton("导出预测结果", self)
        self.exportButton.clicked.connect(self.exportResults)
        layout.addWidget(self.exportButton)

        # 运行并导出结果按钮
        self.runAndExportButton = QPushButton("运行并导出", self)
        self.runAndExportButton.clicked.connect(self.runAndExport)
        layout.addWidget(self.runAndExportButton)

        # 动态命令行输出区域
        self.outputBrowser = QTextBrowser(self)
        layout.addWidget(self.outputBrowser)

        # 设置布局
        self.setLayout(layout)

    def center(self):
        """将窗口居中显示"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def append_output(self, message):
        """动态更新命令行输出"""
        self.outputBrowser.append(message)
        self.outputBrowser.moveCursor(
            self.outputBrowser.textCursor().End
        )  # 自动滚动到末尾

    def loadFile(self):
        """选择数据文件"""
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "选择数据文件",
            "",
            "Excel Files (*.xlsx);;All Files (*)",
            options=options,
        )

        if filePath:
            self.fileLabel.setText(f"已选择文件: {filePath}")
            self.dataPath = filePath
            self.append_output(f"文件选择成功: {filePath}")

    def predictData(self):
        """运行 ARIMA 预测"""
        if hasattr(self, "dataPath"):
            self.append_output("正在加载数据...")
            self.data = load_data(self.dataPath)
            if self.data is not None:
                self.append_output("数据加载成功")
                self.predictionResults = predict_arima(self.data, self.append_output)
            else:
                self.append_output("数据加载失败")
        else:
            self.append_output("请先选择数据文件！")

    def exportResults(self, savePath=None):
        """导出预测结果到指定目录"""
        if hasattr(self, "predictionResults"):
            self.append_output("正在导出结果...")
            if not savePath:
                options = QFileDialog.Options()
                savePath, _ = QFileDialog.getSaveFileName(
                    self,
                    "保存预测结果",
                    "",
                    "Excel Files (*.xlsx);;All Files (*)",
                    options=options,
                )

            if savePath:
                # 保存预测结果到 Excel 文件
                table_output_path = (
                    savePath
                    if savePath.endswith("_表格.xlsx")
                    else savePath.replace(".xlsx", "_表格.xlsx")
                )
                save_results(self.predictionResults, table_output_path)

                # 绘制并保存预测图表
                chart_output_path = table_output_path.replace("_表格.xlsx", "_图表.png")
                plot_predictions(
                    self.data,
                    self.predictionResults,
                    chart_output_path,
                    self.append_output,
                )

                self.append_output(f"预测结果已保存到: {table_output_path}")
        else:
            self.append_output("请先进行预测！")

    def runAndExport(self):
        """运行并导出结果，使用默认命名"""
        if hasattr(self, "dataPath"):
            # 进行预测
            self.predictData()

            # 使用默认的导出路径和命名
            output_directory = os.path.dirname(self.dataPath)
            base_name = "次月燃气使用预测"
            default_excel_path = os.path.join(
                output_directory, f"{base_name}_表格.xlsx"
            )
            self.exportResults(savePath=default_excel_path)
        else:
            self.append_output("请先选择数据文件！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PredictionApp()
    ex.show()
    sys.exit(app.exec_())
