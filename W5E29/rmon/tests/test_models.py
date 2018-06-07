from rmon.models import Server

class  TestServer:
    """Testing Server Function
    """
    def test_save(self,db):
        """Testing Server.save method
        """
        assert Server.query.count() == 0
        server = Server(name='test',host='127.0.0.1')
        server.save()
        assert Server.query.count() == 1
        assert Server.query.first() == server

    def test_delete(self,db,server):
        """Testing Server.delete method
        """
        assert Server.query.count() == 1
        server.delete()
        assert Server.query.count() == 0
