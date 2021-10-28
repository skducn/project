# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2021-10-26
# Description: 用 Python 将 matplotlib 图表集成到 PDF 中
#***************************************************************
from borb.pdf.canvas.color.color import HSVColor, HexColor
from decimal import Decimal
import typing

def create_n_colors(n: int) -> typing.List[str]:
    # The base color is borb-blue
    base_hsv_color: HSVColorHSVColor = HSVColor.from_rgb(HexColor("56cbf9"))
    # This array comprehension creates n HSVColor objects, transforms then to RGB, and then returns their hex string
    return [HSVColor(base_hsv_color.hue + Decimal(x / 360), Decimal(1), Decimal(1)).to_rgb().to_hex_string() for x in range(0, 360, int(360/n))]

# # New import(s)
# import matplotlib.pyplot as plt
# from borb.pdf.canvas.layout.image.chart import Chart
# from borb.pdf.canvas.layout.layout_element import Alignment
# def create_piechart(labels: typing.List[str], data: typing.List[float]):
#     # Symetric figure to ensure equal aspect ratio
#     fig1, ax1 = plt.subplots(figsize=(4, 4))
#     ax1.pie( data,
#         explode=[0 for _ in range(0, len(labels))],
#         labelslabels=labels,
#         autopct="%1.1f%%",
#         shadow=True,
#         startangle=90,
#         colors=create_n_colors(len(labels)),
#         )
#
#     ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
#     return Chart(
#     plt.gcf(),
#     width=Decimal(200),
#     height=Decimal(200),
#     horizontal_alignment=Alignment.CENTERED,
#     )