var coursesList = {
    props: ['courses', 'selected_d', 'selected_c'],
    data: function(){
        return {
            selectedTime: []
        }
    },
    methods: {
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
        'isOK': function(course){
            var time = this.getTime(course.time)
            // console.log(course.name, " ", time)
            for(t of time){
                for(st of this.selectedTime){
                    if(t==st)
                        return false
                }
            }
            return true
        }
    },
    watch: {
        'selected_c': function(){
            var temp = []
            for(var c of this.selected_c){
                temp.push(c.time)
            }
            this.selectedTime = temp
        },
    },
    template: `
    <div>
    <h5>2. 安排課程</h5>
    <table class="table table-striped table-bordered">
        <tr v-for="(course, index) in courses" :key="index"
            v-if="course.department == selected_d">
            <td>
                <div class="container">
                    <div class="row">
                        <b>{{ course.name }} (<a v-bind:href="'https://ccweb.ncnu.edu.tw/student/aspmaker_course_opened_detail_viewview.php?showdetail=&year=1091&courseid='+ course.number +'&_class=' + course.class + '&modal=0'">詳</a>)</b>
                    </div>
                    <div class="row">
                        <div class="col-sm-8">
                            {{ course.teacher }} ‧ {{ course.time }} 
                        </div>
                        <div class="col-sm-4">
                            <button v-if="isOK(course)" type="button" v-on:click="$emit('add-course', course)" class="btn btn-primary">
                                <span>&#43;</span>
                            </button>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
    </table>
    </div>
    `
}