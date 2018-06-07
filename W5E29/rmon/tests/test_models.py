from rmon.models import Server
from rmon.common.rest import RestException

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

    def test_ping_success(self,db,server):
        """Testing the success of Server.ping
        Need to make sure that Redis is listening 127.0.0.1:6379
        """

        assert server.ping() is True

    def test_ping_failed(self,db):
        """Testing the failure of the Server.ping
        When failed on Server.ping will raise the RestException error
        """

        server = Server(name='test',host='127.0.0.1',port=6399)

        try:
            server.ping()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % server.host


