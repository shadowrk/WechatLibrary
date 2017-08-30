from lxml import etree
import datetime
def convertxml(request_xml):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fromuser = request_xml[1].text
    touser = request_xml[0].text
    request_xml[0].text = fromuser
    request_xml[1].text = touser
    request_xml[2].text = now
    #request_xml[4].text = '<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx79532da2a5e44511&redirect_uri=http%3A%2F%2Fwabook.top%2Fwebapp%2Fhome%2F&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect">click</a>'
    request_xml[4].text = '<a href="http://wabook.top/webapp/test/">click</a>'
    # root = etree.Element('xml')
    # child1 = etree.SubElement(root,'ToUserName')
    # child2 = etree.SubElement(root,'FromUserName')
    # child3 = etree.SubElement(root,'CreateTime')
    # child4 = etree.SubElement(root,'MsgType')
    # child5 = etree.SubElement(root,'Content')
    # child1.text = request_xml[1].text
    # child2.text = request_xml[0].text

    # child3.text = now
    # child4.text = 'text'
    #child5.text = '<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx79532da2a5e44511&redirect_uri=http%3A%2F%2Fwabook.top%2Fwebapp%2Fhome%2F&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect">click</a>'

    return request_xml
