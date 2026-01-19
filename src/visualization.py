import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 解决Matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

class DataVisualizer:
    """数据可视化器：生成各类分析图表"""

    def __init__(self, data):
        """
        初始化可视化器
        :param data: 已加载的传感器数据（DataFrame格式）
        """
        self.data = data

    def plot_time_series(self, save_path='docs/timeseries.png'):
        """绘制时间序列图（温度/湿度/PM2.5趋势）"""
        # 创建3个子图（3行1列）
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # 1. 温度趋势
        axes[0].plot(self.data['date'], self.data['temperature'], marker='o', color='red', linewidth=1.5)
        axes[0].set_title('温度变化趋势', fontsize=12)
        axes[0].set_ylabel('温度(℃)', fontsize=10)
        axes[0].grid(True, alpha=0.3)

        # 2. 湿度趋势
        axes[1].plot(self.data['date'], self.data['humidity'], marker='s', color='blue', linewidth=1.5)
        axes[1].set_title('湿度变化趋势', fontsize=12)
        axes[1].set_ylabel('湿度(%)', fontsize=10)
        axes[1].grid(True, alpha=0.3)

        # 3. PM2.5趋势（添加污染界线）
        axes[2].plot(self.data['date'], self.data['pm25'], marker='^', color='green', linewidth=1.5)
        axes[2].set_title('PM2.5变化趋势', fontsize=12)
        axes[2].set_ylabel('PM2.5(μg/m³)', fontsize=10)
        axes[2].set_xlabel('日期', fontsize=10)
        axes[2].grid(True, alpha=0.3)
        # 添加75μg/m³界线（良/轻度污染）
        axes[2].axhline(y=75, color='orange', linestyle='--', label='良/轻度污染界线(75μg/m³)')
        axes[2].legend()

        # 调整子图间距
        plt.tight_layout()
        # 保存图片到docs目录（自动创建目录）
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 时间序列图已保存到：{save_path}")
        # 显示图片
        plt.show()

    def plot_distribution(self, save_path='docs/distribution.png'):
        """绘制数据分布图（直方图+站点对比）"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        # 1. 温度分布直方图
        axes[0, 0].hist(self.data['temperature'], bins=10, color='red', alpha=0.7)
        axes[0, 0].set_title('温度分布', fontsize=12)
        axes[0, 0].set_xlabel('温度(℃)', fontsize=10)

        # 2. 湿度分布直方图
        axes[0, 1].hist(self.data['humidity'], bins=10, color='blue', alpha=0.7)
        axes[0, 1].set_title('湿度分布', fontsize=12)
        axes[0, 1].set_xlabel('湿度(%)', fontsize=10)

        # 3. PM2.5分布直方图
        axes[1, 0].hist(self.data['pm25'], bins=10, color='green', alpha=0.7)
        axes[1, 0].set_title('PM2.5分布', fontsize=12)
        axes[1, 0].set_xlabel('PM2.5(μg/m³)', fontsize=10)
        axes[1, 0].axvline(x=75, color='orange', linestyle='--', label='良/轻度污染界线')
        axes[1, 0].legend()

        # 4. 站点指标对比（柱状图）
        location_avg = self.data.groupby('location')[['temperature', 'humidity', 'pm25']].mean()
        x = range(len(location_avg))
        width = 0.25  # 柱子宽度
        # 温度柱子（左移）
        axes[1, 1].bar([i - width for i in x], location_avg['temperature'], width, label='温度', color='red', alpha=0.7)
        # 湿度柱子（居中）
        axes[1, 1].bar(x, location_avg['humidity'], width, label='湿度', color='blue', alpha=0.7)
        # PM2.5柱子（右移，除以5是为了缩放，方便对比）
        axes[1, 1].bar([i + width for i in x], location_avg['pm25']/5, width, label='PM2.5/5', color='green', alpha=0.7)
        axes[1, 1].set_title('站点指标对比', fontsize=12)
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(location_avg.index)
        axes[1, 1].legend()

        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 分布图已保存到：{save_path}")
        plt.show()

    def plot_correlation(self, save_path='docs/correlation.png'):
        """绘制相关性热图（分析指标间的相关性）"""
        # 计算数值型指标的相关系数
        corr = self.data[['temperature', 'humidity', 'pm25']].corr()

        # 绘制热图
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1, fmt='.2f')
        plt.title('环境指标相关性分析', fontsize=12)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 相关性热图已保存到：{save_path}")
        plt.show()

# 测试代码
if __name__ == '__main__':
    from data_loader import DataLoader

    # 加载数据
    loader = DataLoader()
    data = loader.load_data()

    # 创建可视化器实例
    visualizer = DataVisualizer(data)
    
    # 生成各类图表
    visualizer.plot_time_series()
    visualizer.plot_distribution()
    visualizer.plot_correlation()