"""
环境监测数据分析系统 - 主程序
功能：整合所有模块，一键完成数据加载、分析、可视化
"""

from data_loader import DataLoader
from data_analysis import DataAnalyzer
from visualization import DataVisualizer

def main():
    """主函数：执行完整分析流程"""
    print("="*50)
    print("      环境监测数据分析系统 v1.0")
    print("="*50)

    # 1. 加载数据
    print("\n[1/3] 🔍 加载传感器数据...")
    try:
        loader = DataLoader()
        data = loader.load_data()
        summary = loader.get_summary()
        print(f"✅ 数据加载成功！")
        print(f"   数据规模：{summary['数据形状(行,列)'][0]}行 × {summary['数据形状(行,列)'][1]}列")
        print(f"   监测时间：{summary['日期范围'][0].strftime('%Y-%m-%d')} 至 {summary['日期范围'][1].strftime('%Y-%m-%d')}")
        print(f"   监测站点：{summary['监测站点']}")
    except Exception as e:
        print(f"❌ 数据加载失败：{e}")
        return

    # 2. 数据分析
    print("\n[2/3] 📊 执行数据分析...")
    try:
        analyzer = DataAnalyzer(data)

        print("\n📈 基础统计指标：")
        print(analyzer.basic_statistics())

        print("\n📍 站点对比分析：")
        print(analyzer.location_analysis())

        print("\n🌱 空气质量评估：")
        aq_result = analyzer.air_quality_assessment()
        print(f"   空气质量分布：{aq_result['空气质量分布'].to_dict()}")
        print(f"   优良天数比例：{aq_result['优良天数比例']}")

        print("\n❄️ 温度极值分析：")
        temp_result = analyzer.temperature_extremes()
        for key, value in temp_result.items():
            print(f"   {key}：{value}")
        print("✅ 数据分析完成！")
    except Exception as e:
        print(f"❌ 数据分析失败：{e}")
        return

    # 3. 数据可视化
    print("\n[3/3] 🎨 生成可视化图表...")
    try:
        visualizer = DataVisualizer(data)
        visualizer.plot_time_series()    # 时间序列图
        visualizer.plot_distribution()   # 分布图
        visualizer.plot_correlation()    # 相关性热图
        print("✅ 可视化图表生成完成！")
    except Exception as e:
        print(f"❌ 可视化失败：{e}")
        return

    print("\n🎉 所有分析流程执行完毕！结果已保存到docs目录。")

if __name__ == '__main__':
    # 执行主函数
    main()