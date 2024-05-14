from datetime import datetime


def validate_date_string(date_str, input_format='%d/%m/%Y', output_format='%Y-%m-%d'):
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return False
