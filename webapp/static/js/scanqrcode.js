var timestamp_;
var nonceStr_;
var signature_;
var appid = "wx79532da2a5e44511";
(function(){


  $(".qrcode").bind("click",function () {

     $.ajax({
           url:"../getTest/?url="+window.location.href,
           type:"GET",
           dataType:"JSON",
           success:function(data){
             wx.config({
                 debug: false,  // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
                 appId: appid,// 必填，公众号的唯一标识
                 timestamp: data.timestamp,// 必填，生成签名的时间戳
                 nonceStr: data.nonceStr,// 必填，生成签名的随机串
                 signature: data.signature,// 必填，签名，见附录1
                 jsApiList: [
                     'scanQRCode',
                     //'checkJsApi',
                 ]
                 // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
             });
              wx.ready(function(){
                  //wx.checkJsApi({
                    //  jsApiList: [
                      //    'scanQRCode',
            //
              //        ],
                //      success: function (res) {
                         //  alert(JSON.stringify(res));
                  //    }
                 // });

                 // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，则可以直接调用，不需要放在ready函数中。
                 // mui.alert('微信接口准备就绪');
                 //mui.alert('开始调用扫一扫接口');
                 wx.scanQRCode({
                     needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
                     scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
                     success: function (res) {
                         var result = res.resultStr;
                         //alert(result);
                         window.location.href=result; // 当needResult 为 1 时，扫码返回的结果
                        //  alert(result);
                     }
                 });
           
     });
    }
   });
  });
})();
