
import pytest
from . import server

@pytest.fixture
def clientApp():
  app = server.createApp()
  client =  app.test_client()
  return client
  
 
def test_about(clientApp):
  aboutResponse = clientApp.get('/about')
  aboutResponseLines = aboutResponse.get_data()
  aboutResponseLines = aboutResponseLines.split(b'\n')
  assert aboutResponseLines[0] == b'<!DOCTYPE html>'
