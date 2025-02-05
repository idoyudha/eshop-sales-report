import xlsxwriter
from io import BytesIO
from app.models.sale import SalePublic

def generate_xlsx(sales: list[SalePublic]) -> BytesIO:
    # docs: https://xlsxwriter.readthedocs.io/
    # create an nex excel file and add worksheet
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {"remove_timezone": True})
    worksheet = workbook.add_worksheet()

    # format cells
    bold_format = workbook.add_format({"bold": True})
    money_format = workbook.add_format({'num_format': '$#,##0'})
    datetime_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

    # start from the first cell. rows and columns are zero indexed.
    row, col = 0, 0

    # write headers
    headers = ["no", "user_id", "order_id", "product_id", "quantity", "margin_per_product", "created_at"]
    for header in headers:
        worksheet.write(row, col, header, bold_format)
        col += 1

    row, col = 1, 0
    # write data
    for sale in sales:
        worksheet.write(row, col, row)
        worksheet.write(row, col + 1, str(sale.user_id))
        worksheet.write(row, col + 2, str(sale.order_id))
        worksheet.write(row, col + 3, str(sale.product_id))
        worksheet.write(row, col + 4, sale.product_quantity)
        worksheet.write(row, col + 5, sale.margin_per_product, money_format)
        worksheet.write(row, col + 6, sale.created_at, datetime_format)
        row += 1

    workbook.close()
    output.seek(0)
    return output

