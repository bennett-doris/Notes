function checkLogged(){
    $('#checkLogged').get('/checkLogged',function (data) {
        var html = "";
        if (data.loginStatus == 1){
            html += '<li><a href="/dashboard">控制台</a></li>';
            html += '<li><a href="/logout">退出</a></li>';
        }else{
            html += '<li><a href="/register">注册</a></li>\n' +
                '              <li><a href="/login">登录</a></li>'
        }
        $('#checkLogged').html(html)
    },'json')
}

$(function () {
    checkLogged()
});