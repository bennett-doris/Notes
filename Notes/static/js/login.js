function checkLogin(){
//    检测提交表单的时候是否存在空额表单内容
    var username = $('input[name="username"]');
    var password = $('input[name="password"]');
    alert(username.length);
    if (username.length < 2 || username.length > 20){
        alert('用户名的长度在2-25个字符之间');
        return false;
    }
    if(password.length < 6 || password.length > 20){
        alert('密码的长度在6-20个字符之间');
        return false
    }
}

$(function () {
    checkLogin()
});