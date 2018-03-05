function getConnect() {
    data = $('#addEqForm').serializeArray(); //获取表单所有的input的值
    var dict = {};
    $.each(data, function () {
        dict[this.name] = this.value;
    });
    //dict['csrfmiddlewaretoken'] = '{{ csrf_token }}';
    $.ajax({
        //url: "{% url 'eq_connect' %}",
        url: '/eq/eq_connect',
        type: 'post',
        data: dict,
        success: function (data) {
            console.log(data);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$(function () {
    //处理AJAX CRSF认证开始，此方式使用js单独写在文件里的情况
    jQuery(document).ajaxSend(function (event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
    //处理AJAX CRSF认证结束

    //添加设备调用ajax函数
    $('#eqSubmit').click(
        function () {
            getConnect();
        }
    );

    Vue.use(VueResource); //这里在强调我们用vue-resource.js代替vue.js
    new Vue(
        {
            el: '#app', //绑定的对象是id为app的对象
            data: {
                eq_data: '',
                eq_range: '',
                eq_current:null,
                eq_maxpage:null
            },//绑定的数据,定义数据模型
            created: function () {
                var url = '/eq/eq_list/?page=1';
                this.$http.get(url).then(
                    function (data) {
                        //console.log(data);
                        var Data = data.data;
                        this.eq_data = Data.page_data;
                        this.eq_range = Data.page_range;
                        this.eq_current = Data.current_page;
                        this.eq_maxpage = Data.max_page;
                        console.log(this.eq_maxpage);
                    },//请求成功
                    function (response) {
                        console.log(response);
                    }//请求失败
                )//ajax请求
            },//一个回调函数，默认封装了ajax请求
            methods: {
                getpage: function (page) {
                    var url = '/eq/eq_list/?page=' + page;
                    this.$http.get(url).then(
                        function (data) {
                            //console.log(data);
                            var Data = data.data;
                            this.eq_data = Data.page_data;
                            this.eq_range = Data.page_range;
                            this.eq_current = Data.current_page;
                            this.eq_maxpage = Data.max_page;
                        },//请求成功
                        function (response) {
                            console.log(response);
                        }//请求失败
                    )
                }
            }//用来定义被绑定的方法
        }
    )

});