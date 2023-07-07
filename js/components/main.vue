var mainWindow = {
    data: function () {
        return {
            'courses': [],
            'selectCourses': [],
            'departments': [],
            'selectDepartment': '',
            'foundName': "",
            "user": "",
            'uid': "",
			'name': "",
            'is_print': false,
            'creditNum': 0,
            'year': "1121",
			'token': "",
        }
    },
    created() {
        var main = this
		window.handleCredentialResponse = (response) => {
			var responsePayload = jwt_decode(response.credential)

			main.uid = responsePayload.sub
			main.name = responsePayload.name

			fetch('https://api.snsd0805.com/courseTable?uid=' + this.uid + '&name=' + this.name)
				.then(function (response) {
					return response.json()
				}).then(function (jsonData) {
					console.log(jsonData)
					main.selectCourses = JSON.parse(jsonData['data'])

					var courseSet = new Set()
					for (var course of main.selectCourses) {
						if (!courseSet.has(course.number+course.class)) {   // 用 courseID + 班別 判斷是否重複
							main.creditNum += parseFloat(course.credit)
							courseSet.add(course)
						}
					}
				})
				.catch(function (err) {
					alert("錯誤： " + err)
				})
		}
		window.onload = function () {
			google.accounts.id.initialize({
				client_id: '455078677638-rohoro5d6211r3qt90os459j8ocv86hh.apps.googleusercontent.com',
				callback: handleCredentialResponse
			});
			google.accounts.id.prompt();
		};
		main.getCourseTable()
		console.log("here")
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
        'getCourseTable': function () {
            var main = this
            FB.getLoginStatus(function (response) {
                main.statusChangeCallback(response);
            });
        },
        'saveCourseTable': function () {
            var main = this
            if (this.token != "") {
                filteredCourses = []
                for(var tempCourse of main.selectCourses){
                    if(tempCourse.temp == false){
                        filteredCourses.push(tempCourse);
                    }
                }
                fetch('https://api.snsd0805.com/courseTable', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'token': main.token,
                        'data': filteredCourses
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
            let num;
            const timeRegex = new RegExp(/^\d[\da-z]*[a-z]$/);
            return timeRegex.test(timeString)
                ? [...timeString].reduce((res, c) => {
                    if (Number.isInteger(+c)) {
                        num = c;
                        return res;
                    } else {
                        return [...res, num + c];
                    }
                }, [])
                : [];
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
                    'class': course.class,
                    'credit': course.credit,
                    'link': course.link
                })
            }
            this.creditNum += parseFloat(course.credit)
        },
        'removeCourse': function (course) {
            console.log("remove " + course.name)
            for (var i = this.selectCourses.length - 1; i >= 0; i--) {
                if (this.selectCourses[i].number === course.number && this.selectCourses[i].class === course.class) {
                    this.selectCourses.splice(i, 1)
                }
            }
            this.creditNum -= parseFloat(course.credit)
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
                    a.download = main.year+'課表.jpg';
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
                
				
                <template v-if="uid==''">
					<div id="g_id_onload"
						 data-client_id="455078677638-rohoro5d6211r3qt90os459j8ocv86hh.apps.googleusercontent.com"
						 data-context="signin"
						 data-ux_mode="popup"
						 data-callback="handleCredentialResponse"
						 data-auto_prompt="false">
					</div>

					<div class="g_id_signin"
						 data-type="standard"
						 data-shape="pill"
						 data-theme="outline"
						 data-text="signin_with"
						 data-size="large"
						 data-logo_alignment="left">
					</div>
				</template>
				<template v-else>
                	<li class="nav-item mx-0 mx-lg-1"><a class='nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger'>Hi, {{ this.name }}</a></li>
				</template
				
            </ul>
        </div>
    </div>
</nav>
<br><br>


<section class="page-section portfolio" id="portfolio">
    <div class="container" id='table'>
        <!-- Portfolio Section Heading-->
        <h2 class="page-section-heading text-center text-uppercase text-secondary mb-0">{{ year }} 課表</h2>

        <!-- Icon Divider-->
        <div class="divider-custom">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>
        <div class="divider-custom">
            <div class="row">
                <div class="col-4">
                    <div v-if="uid!=''"><button class="btn btn-danger" @click="saveCourseTable()">儲存</button></div>
                    <div v-if="uid==''"><button class="btn btn-danger btn-disable" @click="saveCourseTable()">儲存(請先登入Google)</button></div>
                </div>
                <div class="col-4">
                    <div><button class="btn btn-success" @click="generatePic()">下載圖檔</button></div>
                </div>
                <div class="col-4">
                    <div><button class="btn btn-primary" @click="share()">分享課表</button></div>
                </div>
            </div>
        </div>
		Facebook變動開發者權限規範，目前狀況無法排除...部份使用者無法進行Facebook登入，搶修中...
		<br>
		<strong>Google登入功能測試中，請不要點選...工程師半夜正在加班中...</strong>
        <br>
		<br><br>
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
                <div class="row">
                    <div class="col">
                        <div class="card">
                            <div class="card-body">
                                已經選了 {{ creditNum }} 學分
                            </div>
                        </div>
                    </div>
                </div>
                <p class="text-sm-left"></p>
            </div>
            
            <br>
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
                    <li>已經更新成 1121 新學期課表</li>
					<li><strong>Facebook變動開發者權限規範，目前狀況無法排除...無法進行Facebook登入，搶修中...</strong></li>
                    <li>有發現 Bug 可以到 <a href='https://github.com/snsd0805/NCNU_Course/issues'>GitHub</a> 發 issue 或 <a href='mailto:levi900227@gmail.com'>mail</a></li>
                </ul>
                2023 06/19 更新
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
                https://course.snsd0805.com/#/share/{{user.id}}
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
