"""Small helper functions to convert US Units to Metric


"""


US_FOOT_TO_METER_CONVERSION_FACTOR = 0.3048
US_INCH_TO_METER_CONVERSION_FACTOR = 0.0254


def feet2m(feet):
    return US_FOOT_TO_METER_CONVERSION_FACTOR * feet


def inch2m(inches):
    return US_INCH_TO_METER_CONVERSION_FACTOR * inches


def us_hight2m(feet, inches):
    return feet2m(feet) + inch2m(inches)


def m2cm(meters):
    return meters * 100


def cm2m(centimeters):
    return centimeters / 100

