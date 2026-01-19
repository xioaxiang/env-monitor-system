import pandas as pd
import os

class DataLoader:
    """数据加载器：负责读取和预处理传感器数据"""

    def __init__(self, data_path='data/sensor_data.csv'):
        """
        初始化数据加载器
        :param data_path: 数据文件路径（默认在data目录）
        """
        self.data_path = data_path
        self.data = None  # 存储加载后的数据

    def load_data(self):
        """加载CSV数据，并将date列转为日期格式"""
        # 检查文件是否存在
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"数据文件不存在，请检查路径：{self.data_path}")

        # 读取CSV文件
        self.data = pd.read_csv(self.data_path, encoding='utf-8')
        # 转换日期格式
        self.data['date'] = pd.to_datetime(self.data['date'])
        return self.data

    def get_data(self):
        """获取加载后的数据（若未加载则自动加载）"""
        if self.data is None:
            self.load_data()
        return self.data

    def get_summary(self):
        """获取数据摘要信息（维度、列名、日期范围、监测站点）"""
        if self.data is None:
            self.load_data()
        
        return {
            '数据形状(行,列)': self.data.shape,
            '列名': list(self.data.columns),
            '日期范围': (self.data['date'].min(), self.data['date'].max()),
            '监测站点': self.data['location'].unique().tolist()
        }

# 测试代码（仅在直接运行该文件时执行）
if __name__ == '__main__':
    # 创建数据加载器实例
    loader = DataLoader()
    # 加载数据
    data = loader.load_data()
    print("✅ 数据加载成功！")
    print("数据前5行：")
    print(data.head())
    
    print("\n📊 数据摘要:")
    summary = loader.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")