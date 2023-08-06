from pysasl import sasl_prep

def test_sasl_prep():
    assert "test" == sasl_prep("test")
    assert "éøçû" == sasl_prep("éøçû")

