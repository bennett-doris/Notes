$(function () {
//     检测邮箱是否已被注册
//    设置一个标志，决定是否可以提交
    window.registerMsg = 1;
    $("#form-check").blur(function () {
    //    当鼠标移开时，先判断表单里是否有输入
   //    如果没有输入，则直接返回，无需与后端进行交互
        if ($(this).val().trim().length == 0)
            return;
    //    如果有内容，则发送ajax请求进行检查
        $.get('check_info',{'email':$(this).val()},function (data){
            $('.inspect').html(data.msg);
            window.registerMsg = data.status;
    },'json')});

//    为整个表单绑定submit事件，确定是否提交
    $('#formReg').submit(function () {
        if (window.registerMsg == 1) {
            return False;
        }
        return True;
    })
});
