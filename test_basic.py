
import pytest

@pytest.fixture
def clientApp(app):
  client =  app.test_client()
  return client
  
 
def test_about(clientApp):
  aboutResponse = clientApp.get('/about')
  aboutResponseLines = aboutResponse.split('\n')
  assert aboutResponseLines[0] == '<!DOCTYPE html>'
