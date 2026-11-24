from aiovoip.message import Message, Request, Response

RAW_REQUEST = (
    b'OPTIONS sip:pytest@127.0.0.1:7000 SIP/2.0\r\n'
    b'Via: SIP/2.0/UDP 127.0.0.1:7001;branch=z9hG4bKabc123\r\n'
    b'From: <sip:client@127.0.0.1:7001>;tag=abc\r\n'
    b'To: <sip:pytest@127.0.0.1:7000>\r\n'
    b'Call-ID: cseq-zero-test\r\n'
    b'CSeq: 0 OPTIONS\r\n'
    b'Contact: <sip:client@127.0.0.1:7001>\r\n'
    b'Max-Forwards: 70\r\n'
    b'Content-Length: 0'
)


def test_parse_request_with_cseq_zero():
    request = Message.from_raw_headers(RAW_REQUEST)
    assert isinstance(request, Request)
    assert request.cseq == 0
    assert request.method == 'OPTIONS'


def test_response_from_request_with_cseq_zero():
    request = Message.from_raw_headers(RAW_REQUEST)
    response = Response.from_request(request, 200, 'OK')
    assert response.cseq == 0
    assert b'CSeq: 0 OPTIONS' in response.encode()
