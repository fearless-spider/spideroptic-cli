
from spideroptic.main import SpiderOpticTest

def test_spideroptic(tmp):
    with SpiderOpticTest() as app:
        res = app.run()
        print(res)
        raise Exception

def test_command1(tmp):
    argv = ['command1']
    with SpiderOpticTest(argv=argv) as app:
        app.run()
