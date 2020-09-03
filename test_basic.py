
import pytest

@pytest.fixture
def client(app):
  clientApp =  app.test_client()
    
  aboutResponse = clientApp.get('/about')
  aboutResponseLines = aboutResponse.split('\n')
  assert aboutResponseLines[0] == '<!DOCTYPE html>'
