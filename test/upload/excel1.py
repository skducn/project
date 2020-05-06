# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-12-19
# Description: excel

# http://www.cnblogs.com/snow-backup/p/4021554.html
# python处理Excel，pythonexcel http://www.bkjia.com/Pythonjc/926154.html

# 一、可使用的第三方库

# python中处理excel表格，常用的库有xlrd（读excel）表、xlwt（写excel）表、openpyxl（可读写excel表）等。xlrd读数据较大的excel表时效率高于openpyxl，
# 所以我在写脚本时就采用了xlrd和xlwt这两个库。介绍及下载地址为：http: // www.python - excel.org / 这些库文件都没有提供修改现有excel表格内容的功能。
# 一般只能将原excel中的内容读出、做完处理后，再写入一个新的excel文件。

# 二、常见问题
#
# 使用python处理excel表格时，发现两个个比较难缠的问题：unicode编码和excel中记录的时间。
#
# 因为python的默认字符编码都为unicode，所以打印从excel中读出的中文或读取中文名的excel表或sheet时，程序提示错误UnicodeEncodeError: 'ascii'
# codeccan't encode characters in position 0-2: ordinal not in range(128)。' \
# '这是由于在windows中，中文使用了gb2312编码方式，python将其当作unicode和ascii来解码都不正确才报出的错误。使用VAR.encode('
# gb2312')即可解决打印中文的问题。（很奇怪，有的时候虽然能打印出结果，但显示的不是中文，而是一堆编码。）若要从中文文件名的excel表中读取数据，可在文件名前加‘u’表示将该中文文件名采用unicode编码。
#
# 有excel中，时间和日期都使用浮点数表示。可看到，当‘2013
# 年3月20日’所在单元格使用‘常规’格式表示后，内容变为‘41353’；当其单元格格式改变为日期后，内容又变为了‘2013
# 年3月20日’。而使用xlrd读出excel中的日期和时间后，得到是的一个浮点数。所以当向excel中写入的日期和时间为一个浮点数也不要紧，只需将表格的表示方式改为日期和时间，即可得到正常的表示方式。excel中，用浮点数1表示1899年12月31日。
# ********************************************************************************************************************


import xlrd


def read(filename, sheetNo=0):
    book = xlrd.open_workbook(filename)
    sh = book.sheet_by_index(sheetNo)
    cols = sh.ncols
    rows = sh.nrows
    print 'cols=', cols, 'rows=', rows
    for r in range(rows):  # cols and rows start from 0
        value = sh.cell_value(rowx=r, colx=0)




# 　　http: // nullege.com / codes / search / xlwt.easyxf

# 最简单的例子
import xlwt

workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet('My Worksheet')
worksheet.write(0, 0, label='Row 0, Column 0 Value')
workbook.save('Excel_Workbook.xls')

# 格式化cell的font
font = xlwt.Font()  # Create the Font
font.name = 'Times New Roman'
font.bold = True
font.underline = True
font.italic = True
style = xlwt.XFStyle()  # Create the Style
style.font = font  # Apply the Font to the Style
worksheet.write(0, 0, label='Unformatted value')
worksheet.write(1, 0, label='Formatted value', style)  # Apply the Style to the Cell

# Font对象的属性
font.bold = True  # May be: True, False
font.italic = True  # May be: True, False
font.struck_out = True  # May be: True, False
font.underline = xlwt.Font.UNDERLINE_SINGLE  # May be: UNDERLINE_NONE, UNDERLINE_SINGLE, UNDERLINE_SINGLE_ACC, UNDERLINE_DOUBLE, UNDERLINE_DOUBLE_ACC
font.escapement = xlwt.Font.ESCAPEMENT_SUPERSCRIPT  # May be: ESCAPEMENT_NONE, ESCAPEMENT_SUPERSCRIPT, ESCAPEMENT_SUBSCRIPT
font.family = xlwt.Font.FAMILY_ROMAN  # May be: FAMILY_NONE, FAMILY_ROMAN, FAMILY_SWISS, FAMILY_MODERN, FAMILY_SCRIPT, FAMILY_DECORATIVE
font.charset = xlwt.Font.CHARSET_ANSI_LATIN  # May be: CHARSET_ANSI_LATIN, CHARSET_SYS_DEFAULT, CHARSET_SYMBOL, CHARSET_APPLE_ROMAN, CHARSET_ANSI_JAP_SHIFT_JIS, CHARSET_ANSI_KOR_HANGUL, CHARSET_ANSI_KOR_JOHAB, CHARSET_ANSI_CHINESE_GBK, CHARSET_ANSI_CHINESE_BIG5, CHARSET_ANSI_GREEK, CHARSET_ANSI_TURKISH, CHARSET_ANSI_VIETNAMESE, CHARSET_ANSI_HEBREW, CHARSET_ANSI_ARABIC, CHARSET_ANSI_BALTIC, CHARSET_ANSI_CYRILLIC, CHARSET_ANSI_THAI, CHARSET_ANSI_LATIN_II, CHARSET_OEM_LATIN_I
font.colour_index = 2  # 0:black, 1: white, 2: red, 3:light green, 4:blue
font.get_biff_record = ?
font.height = 0x00C8  # C8 in Hex (in decimal) = 10 points in height.
font.name = ?
font.outline = ?
font.shadow = ?


# 设置cell的宽度
worksheet.write(0, 0, 'My Cell Contents')
worksheet.col(0).width = 3333  # 3333 = 1" (one inch).

# 向cell添加一个日期
style = xlwt.XFStyle()
style.num_format_str = 'M/D/YY'  # Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
worksheet.write(0, 0, datetime.datetime.now(), style)

# 向cell添加一个Formula
worksheet.write(0, 0, 5)  # Outputs 5
worksheet.write(0, 1, 2)  # Outputs 2
worksheet.write(1, 0, xlwt.Formula('A1*B1'))  # Should output "10" (A1[5] * A2[2])
worksheet.write(1, 1, xlwt.Formula('SUM(A1,B1)'))  # Should output "7" (A1[5] + A2[2])

# 向cell添加一个Hyperlink
worksheet.write(0, 0, xlwt.Formula(
    'HYPERLINK("http://www.google.com";"Google")'))  # Outputs the text "Google" linking to http://www.google.com

# 合并行列
worksheet.write_merge(0, 0, 0, 3, 'First Merge')  # Merges row 0's columns 0 through 3.
font = xlwt.Font()  # Create Font
font.bold = True  # Set font to Bold
style = xlwt.XFStyle()  # Create Style
style.font = font  # Add Bold Font to Style
worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style)  # Merges row 1 through 2's columns 0 through 3.

# 设置cell内部定位
alignment = xlwt.Alignment()  # Create Alignment
alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
style = xlwt.XFStyle()  # Create Style
style.alignment = alignment  # Add Alignment to Style
worksheet.write(0, 0, 'Cell Contents', style)

# 添加cell的边框
# Please note: While I was able to find these constants within the source code, on my system (using LibreOffice,) I was only presented with a solid line, varying from thin to thick; no dotted or dashed lines.
borders = xlwt.Borders()  # Create Borders
borders.left = xlwt.Borders.DASHED  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
borders.right = xlwt.Borders.DASHED
borders.top = xlwt.Borders.DASHED
borders.bottom = xlwt.Borders.DASHED
borders.left_colour = 0x40
borders.right_colour = 0x40
borders.top_colour = 0x40
borders.bottom_colour = 0x40
style = xlwt.XFStyle()  # Create Style
style.borders = borders  # Add Borders to Style
worksheet.write(0, 0, 'Cell Contents', style)

# 设置cell的背景颜色
pattern = xlwt.Pattern()  # Create the Pattern
pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
pattern.pattern_fore_colour = 5  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
style = xlwt.XFStyle()  # Create the Pattern
style.pattern = pattern  # Add Pattern to Style
worksheet.write(0, 0, 'Cell Contents', style)

# TODO: Things
# Left
# to
# Document
# - Panes - - separate
# views
# which
# are
# always in view
# - Border
# Colors(documented
# above, but
# not taking
# effect as it
# should)
# - Border
# Widths(document
# above, but
# not working as expected)
# - Protection
# - Row
# Styles
# - Zoom / Manification
# - WS
# Props?
# Source
# Code
# for reference available at: https: // secure.simplistix.co.uk / svn / xlwt / trunk / xlwt /
# 复制代码
