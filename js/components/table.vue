var courseDiv = {
    props: ['course', 'is_shared', 'is_print'],
    template: `
        <div style='border: 5px #1abc9c solid; text-align: center;'>
            {{ course.name }}
            <template v-if='course.time == "另訂"'>
                - {{ course.teacher }} 老師
            </template>
            <a v-bind:href="course.link" target="_blank"><i class="fas fa-info-circle"></i></a>
            <button type="button" 
                v-if="!is_shared"
                v-on:click="$emit('remove-course', course)"
                class="btn btn-danger btn-sm"
                :style="{'display': is_print ? 'none' : 'inline-block'}"
           >
                刪
            </button>
        </div> 
    `
}
var tempDiv = {
    props: ['course'],
    template: `
        <div style='border: 5px #cf1d5e solid; text-align: center;'>
            {{ course.name }}
        </div> 
    `
}
var courseTable = {
    props: ['select_c', 'is_shared', 'is_print'],
    data: function(){
        return {
            'courses': {},
            'coursesWithoutTime': [],
            'existWeekend': false
        }
    },
    methods: {
        'exist': function(time){
            for(var c of this.select_c){
                if(c.time==time){
                    this.course = c
                    return true
                }
            }
            return false
        },
        'removeCourseHandler': function(course){
            this.$emit('remove-course', course)
        }
    },
    watch: {
        'select_c': function(){
            this.courses = {}
            this.coursesWithoutTime = []
            var weekendLock = false

            for(var c of this.select_c){
                if(c.time != '另訂'){
                    this.courses[c.time] = {
                        'name': c.name,
                        'number': c.number,
                        'class': c.class,
                        'temp': c.temp,
                        'credit': c.credit,
                        'link': c.link,
                        'time': c.time,
                        'teacher': c.teacher,
                    }
                } else {
                    this.coursesWithoutTime.push({
                        'name': c.name,
                        'number': c.number,
                        'class': c.class,
                        'temp': c.temp,
                        'credit': c.credit,
                        'link': c.link,
                        'time': c.time,
                        'teacher': c.teacher,
                    })
                }

                if(c.time[0]==6 || c.time[0]==7){
                    weekendLock = true
                }
            }
            if(weekendLock){
                this.existWeekend = true
            }else{
                this.existWeekend = false
            }
        }
    },
    components: {
        'course-div': courseDiv,
        'temp-div': tempDiv
    },
    template: `
<div>
    <table class="table table-bordered" style="table-layout: fixed;word-wrap: break-word;">
        <thead>
            <th scope="col" class="col-md-1">#</th>
            <th scope="col" class="col-md-2">一</th>
            <th scope="col" class="col-md-2">二</th>
            <th scope="col" class="col-md-2">三</th>
            <th scope="col" class="col-md-2">四</th>
            <th scope="col" class="col-md-2">五</th>
            <template v-if='existWeekend'>
                <th scope="col" class="col-md-1">六</th>
                <th scope="col" class="col-md-1">日</th>
            </template>
            </tr>
        </thead>
        <tbody>
            <tr v-for="hour in 13">
                <template v-if="hour+7==12">
                    <th style='text-align: center;' scope='row'>
                        {{ hour+7 }}~{{ hour+8 }}  <br> z
                    </th>
                    
                    <td style='text-align: center; background-color: #1abc9c;'
                        v-for="week in (existWeekend)?7:5">
                        <course-div 
                            v-if="exist(week+'z')"
                            v-bind:course="courses[week+'z']"
                            v-bind:is_shared="is_shared"
                            v-on:remove-course="removeCourseHandler"
                        ></course-div>
                        
                    </td>
                </template>
                <template v-else>
                    <th style='text-align: center;' scope='row'>
                        {{ hour+7 }} ~ {{ hour+8 }}   <br>
                        {{ String.fromCharCode(97+((hour<5)?(hour-1):(hour-2))) }}
                    </th>
                    <td v-for='week in (existWeekend)?7:5'>
                        <course-div 
                            v-if="exist(week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))) && !courses[week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))].temp"
                            v-bind:course="courses[week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))]"
                            v-bind:is_shared="is_shared"
                            v-bind:is_print="is_print"
                            v-on:remove-course="removeCourseHandler"
                        ></course-div>
                        <temp-div 
                            v-if="exist(week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))) && courses[week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))].temp"
                            v-bind:course="courses[week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))]"
                        ></temp-div>
                    </td>
                </template>
            </tr>
        </tbody>
    </table>
	<br><br>
    <table class="table table-bordered" style="table-layout: fixed;word-wrap: break-word;">
        <thead>
            <tr>
                <th scope="col" class="col-md-1 text-center">時間未定</th>
            </tr>
        </thead>
        <tbody>
            <template v-if='coursesWithoutTime.length == 0'>
                <tr>
                    <td class='text-center'>
                        您目前沒有時間未定的課程
                    </td>
                </tr>
            </template>
            <template v-for='course in coursesWithoutTime'>
                <tr>
                    <td>
                        <course-div 
                            v-bind:course="course"
                            v-bind:is_shared="is_shared"
                            v-bind:is_print="is_print"
                            v-on:remove-course="removeCourseHandler"
                        ></course-div>
                    </td>
                </tr>
            </template>
        </tbody>
    </table>
</div>
    `
}
