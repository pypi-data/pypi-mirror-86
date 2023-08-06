from net_speed_checker import check_speed


def test_empty():
    check_speed.measure(
        'mysql',
        'pf_admin',
        'net_speed_checker',
        'pf-mysql.cmlcmyajg2ee.eu-west-2.rds.amazonaws.com:55511',
        '3N!ovUuX8rCUPeKw8YWrSa9g*X1^YGik8XCEfEIh')
