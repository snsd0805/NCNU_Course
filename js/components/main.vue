var mainWindow = {
    data: function () {
        return {
            'courses': [],
            'selectCourses': [],
            'departments': [],
            'selectDepartment': '',
            'foundName': "",
            "user": "",
            'token': "",
            'is_print': false,
        }
    },
    created() {
        var main = this
        window.fbAsyncInit = function () {
            FB.init({
                appId: '',
                cookie: true,
                xfbml: true,
                version: 'v9.0'
            });

            FB.AppEvents.logPageView();
            main.getCourseTable()
        };

        (function (d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) { return; }
            js = d.createElement(s); js.id = id;
            js.src = "https://connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    },
    mounted() {
        var main = this
        axios
            .get("./output.json")
            .then(response => (main.courses = response.data))
            .then(function () {
                for (var course of main.courses) {
                    // console.log(course.name)
                    if (main.departments.indexOf(course.department) == -1) {
                        main.departments.push(course.department)
                    }
                }
            })
            .then(function () {
                main.departments.sort()
                main.selectDepartment = main.departments[15]
            })
        // Collapse Navbar
        var navbarCollapse = function () {
            if ($("#mainNav").offset().top > 100) {
                $("#mainNav").addClass("navbar-shrink");
            } else {
                $("#mainNav").removeClass("navbar-shrink");
            }
        };
        // Collapse now if page is not at top
        navbarCollapse();
        // Collapse the navbar when page is scrolled
        $(window).scroll(navbarCollapse);
    },
    methods: {
        'login': function () {
            var main = this
            FB.login(function () {
                main.getCourseTable()
            })
        },
        'logout': function () {
            var main = this
            FB.logout(function (response) {
                main.user = ""
                main.token = ""
            });
        },
        'getCourseTable': function () {
            var main = this
            FB.getLoginStatus(function (response) {
                main.statusChangeCallback(response);
            });
        },
        'statusChangeCallback': function (response) {
            if (response.status == "connected") {
                this.token = response.authResponse.accessToken

                var main = this
                FB.api('/me', function (response) { main.user = response })

                fetch('https://api.snsd0805.com/courseTable?token=' + this.token)
                    .then(function (response) {
                        return response.json()
                    }).then(function (jsonData) {
                        console.log(jsonData)
                        main.selectCourses = JSON.parse(jsonData['data'])
                    })
                    .catch(function (err) {
                        alert("錯誤： " + err)
                    })
            }
        },
        'saveCourseTable': function () {
            var main = this
            if (this.token != "") {
                fetch('https://api.snsd0805.com/courseTable', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'token': main.token,
                        'data': main.selectCourses
                    })
                })
                    .then(function (response) {
                        return response.json()
                    })
                    .then(function (response) {
                        if (response.status == "saved") {
                            alert("已儲存")
                        } else {
                            alert("錯誤")
                        }
                    })
                    .catch(function (err) {
                        alert("錯誤： " + err)
                    })

            } else {
                this.login()
            }
        },
        'getTime': function (timeString) {
            ans = []
            number = ""
            for (var i of timeString) {
                if (i >= "0" && i <= "9") {
                    number = i
                } else if (i >= "a" && i <= "z") {
                    ans.push(number + i)
                }
                else {
                    ans.push(timeString)
                    break
                }
            }
            return ans
        },
        'select': function (department) {
            this.selectDepartment = department
        },
        'founded': function (courseName) {
            this.foundName = courseName
        },
        'addCourse': function (course) {
            var time = this.getTime(course.time)
            for (var t of time) {
                this.selectCourses.push({
                    'time': t,
                    'name': course.name,
                    'temp': false,
                    'number': course.number,
                    'class': course.class
                })
            }
        },
        'removeCourse': function (course) {
            console.log("remove " + course.name)
            for (var i = this.selectCourses.length - 1; i >= 0; i--) {
                if (this.selectCourses[i].number === course.number && this.selectCourses[i].class === course.class) {
                    this.selectCourses.splice(i, 1)
                }
            }
        },
        'saveTemp': function (course) {
            if (course == null) {
            } else {
                this.tempCourse = []
                var time = this.getTime(course.time)
                for (var t of time) {
                    this.selectCourses.push({
                        'time': t,
                        'name': course.name,
                        'temp': true
                    })
                }
            }
        },
        'deleteTemp': function (course) {
            for (var i = this.selectCourses.length - 1; i >= 0; i--) {
                if (this.selectCourses[i].name == course.name && this.selectCourses[i].temp == true) {
                    this.selectCourses.splice(i, 1)
                }
            }
        },
        'generatePic': function () {
            var main = this
            const doPrint = new Promise((resolve, reject) => {
                main.is_print = true;
                resolve();
            });
            doPrint
            .then(() =>{
                html2canvas(document.getElementById('course-table-div')).then(function (canvas) {
                    var a = document.createElement('a');
                    a.href = canvas.toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
                    a.download = '課表.jpg';
                    a.click();
                });
            })
            .then(() => {
                main.is_print = false;
            })
        },
        'share': function () {
            if (this.user != "")
                $('#share').modal('show');
            else
                this.login()
        },
    },
    components: {
        'course-table': courseTable,
        'choose-department': chooseDepartment,
        'course-anslist': coursesList
    },
    template: `
    <div>
<!-- Navigation-->
<nav class="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top" id="mainNav">
    <div class="container">
        <a class="navbar-brand js-scroll-trigger" href="#page-top">暨大排課表</a>
        <button class="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white rounded" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            Menu
            <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item mx-0 mx-lg-1"><a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger" href="https://github.com/snsd0805/NCNU_Course">Github</a></li>
                
                <li v-if="token==''" class="nav-item mx-0 mx-lg-1"><a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger" href='#' v-on:click="login()">Facebook登入</a></li>
                <li v-if="token!=''" class="nav-item mx-0 mx-lg-1"><a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger" href="#" v-on:click="logout()">登出Facebook—{{user.name}}</a></li>

            </ul>
        </div>
    </div>
</nav>
<br><br>


<section class="page-section portfolio" id="portfolio">
    <div class="container" id='table'>
        <!-- Portfolio Section Heading-->
        <h2 class="page-section-heading text-center text-uppercase text-secondary mb-0">課表</h2>
        <!-- Icon Divider-->
        <div class="divider-custom">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>
        <div class="divider-custom">
            <div class="row">
                <div class="col-4">
                    <div v-if="token!=''"><button class="btn btn-danger" @click="saveCourseTable()">儲存</button></div>
                    <div v-if="token==''"><button class="btn btn-danger" @click="saveCourseTable()">儲存(登入FB)</button></div>
                </div>
                <div class="col-4">
                    <div><button class="btn btn-success" @click="generatePic()">下載圖檔</button></div>
                </div>
                <div class="col-4">
                    <div><button class="btn btn-primary" @click="share()">分享課表</button></div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-3">
                <div class="row mx-auto mb-2">
                    <choose-department 
                        v-bind:departments="departments"
                        v-bind:selected="selectDepartment"
                        v-on:selectok="select"
                        v-on:foundedok="founded"
                    >
                    </choose-department>
                </div>
                <br>
                <div class="row mx-auto mb-2">
                    <course-anslist
                        v-bind:courses="courses"
                        v-bind:selected_d="selectDepartment"
                        v-bind:selected_c="selectCourses"
                        v-bind:find_name="foundName"
                        v-on:add-course="addCourse"
                        v-on:show-temp="saveTemp"
                        v-on:delete-temp="deleteTemp"
                    >
                    </course-anslist>
                </div>
            </div>

            <div class="col-lg-9 table-responsive " >
                <course-table
                    id="course-table-div"
                    v-bind:selectCourses="selectCourses"
                    v-bind:select_c="selectCourses"
                    v-bind:is_print="is_print"
                    v-bind:is_shared="false"
                    v-on:remove-course="removeCourse"
                ></course-table>
            </div>
        </div>
        <!-- Portfolio Grid Items-->
    </div>
</section>


<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">資訊公告</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body">
                <ul>
                    <li>已經更新為 1092 新課表(包含通識課分類)</li>
                    <li>使用 Facebook API 儲存課表</li>
                    <li>新增「下載圖檔」功能</li>
                    <li>新增「分享課表」功能</li>
                </ul>
                2021 01/23 更新
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">我知道了</button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="share" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">分享課表</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body">
                請複製以下網址給你的朋友，跟他分享你的課表<br><br>
                https://snsd0805.com/NCNU_Course/#/share/{{user.id}}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">我知道了</button>
            </div>
        </div>
    </div>
</div>
</div>
</div>
    `
}