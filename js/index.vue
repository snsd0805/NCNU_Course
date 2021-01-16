var vm = new Vue({
    el: "#main",
    data: {
        'courses': [],
        'selectCourses': [],
        'departments': [],
        'selectDepartment': '',
        'foundName': "",
        "user": "",
        'token': ""
    },
    created() {
        window.fbAsyncInit = function() {
            FB.init({
                appId      : '',
                cookie     : true,
                xfbml      : true,
                version    : 'v9.0'
            });
                
            FB.AppEvents.logPageView();
            vm.getCourseTable()
        };
      
        (function(d, s, id){
           var js, fjs = d.getElementsByTagName(s)[0];
           if (d.getElementById(id)) {return;}
           js = d.createElement(s); js.id = id;
           js.src = "https://connect.facebook.net/en_US/sdk.js";
           fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    },
    mounted() {
        axios
            .get("./output.json")
            .then(response => (vm.courses = response.data))
            .then(function(){
                for(var course of vm.courses){
                    // console.log(course.name)
                    if(vm.departments.indexOf(course.department)==-1){
                        vm.departments.push(course.department)
                    }
                }
            })
            .then(function(){
                vm.departments.sort()
                vm.selectDepartment = vm.departments[15]
            })
    },
    methods: {
        'login': function(){
            FB.login(function(){
                vm.getCourseTable()
            })
        },
        'logout': function(){
            FB.logout(function(response) {
                vm.user = ""
                vm.token = ""
            });
        },
        'getCourseTable': function(){
            FB.getLoginStatus(function(response) {
                vm.statusChangeCallback(response);
            });
        },
        'statusChangeCallback': function(response){
            if(response.status == "connected"){
                this.token = response.authResponse.accessToken

                FB.api('/me', function(response){vm.user = response.name})

                fetch('https://api.snsd0805.com/courseTable?token='+this.token)
                    .then(function(response){
                        return response.json()
                    }).then(function(jsonData){
                        console.log(jsonData)
                        vm.selectCourses = JSON.parse(jsonData['data'])
                    })
                    .catch(function(err){
                        alert("錯誤： "+err)
                    })
            }
        },
        'saveCourseTable': function(){
            if(this.token!=""){
                fetch('https://api.snsd0805.com/courseTable',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'token': vm.token,
                        'data': vm.selectCourses
                    })
                })
                    .then(function(response){
                        return response.json()
                    })
                    .then(function(response){
                        if(response.status=="saved"){
                            alert("已儲存")
                        }else{
                            alert("錯誤")
                        }
                    })
                    .catch(function(err){
                        alert("錯誤： "+err)
                    })

            }else{
                this.login()
            }
        },
        'getTime': function(timeString){
            ans = []
            number = ""
            for(var i of timeString){
                if(i>="0" && i<="9"){
                    number = i
                }else if(i>="a" && i<="z"){
                    ans.push(number+i)
                }
                else{
                    ans.push(timeString)
                    break
                }
            }
            return ans
        },
        'select': function(department){
            this.selectDepartment = department
        },
        'founded': function(courseName){
            this.foundName = courseName
        },
        'addCourse': function(course){
            var time = this.getTime(course.time)
            for(var t of time){
                this.selectCourses.push({
                    'time': t,
                    'name': course.name,
                    'temp': false
                })
            }
        },
        'removeCourse': function(course){
            console.log("remove "+course)
            for(var i=this.selectCourses.length-1;i>=0;i--){
                if(this.selectCourses[i].name == course){
                    this.selectCourses.splice(i, 1)
                }
            }
        },
        'saveTemp': function(course){
            if(course==null){
            }else{
                this.tempCourse = []
                var time = this.getTime(course.time)
                for(var t of time){
                    this.selectCourses.push({
                        'time': t,
                        'name': course.name,
                        'temp': true
                    })
                }
            }
        },
        'deleteTemp': function(course){
            for(var i=this.selectCourses.length-1;i>=0;i--){
                if(this.selectCourses[i].name == course.name && this.selectCourses[i].temp == true){
                    this.selectCourses.splice(i, 1)
                }
            }
        },
    },
    components: {
        'course-table': courseTable,
        'choose-department': chooseDepartment,
        'course-anslist': coursesList,
        
    }
})





// 'update': function(){
//     this.tableBody = ""
//     for(var hour=8;hour<=21;hour++){
//         // console.log(hour)
//         symbolIndex = (hour<12)?(hour-8):(hour-9)
//         this.tableBody += "<tr>"
//         if(hour==12){       //處理中午時段
//             this.tableBody += "<th style='text-align: center;' scope='row'>"+hour+"~"+(hour+1)+"<br>z</th>"
//             this.tableBody += "<td style='text-align: center; background-color: #1abc9c;' colspan='5'>中午休息時間</td>"

//             continue
//         }else{
//             this.tableBody += "<th style='text-align: center;' scope='row'>"+hour+"~"+(hour+1)+"<br>"+String.fromCharCode(97+symbolIndex)+"</th>"
//         }
        
//         for(var week=1;week<=5;week++){
//             this.tableBody += "<td>"
//             // console.log(symbolIndex)
//             var course = this.exist(week+String.fromCharCode(97+symbolIndex))
//             if(course){
//                 this.tableBody += "<div style='border: 5px #1abc9c solid; text-align: center;'>"
//                 // console.log(week+String.fromCharCode(97+(hour-8)))
//                 this.tableBody += course.name+' <button type="button" v-on:click=\"$emit(\'remove\', course)\" class="btn btn-danger btn-sm">刪</button>'
//             }
//             this.tableBody += "</td>"
//         }
//         this.tableBody += "</tr>"
//     }
//     this.tableBody += "</tbody>"
// }