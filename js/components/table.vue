var courseDiv = {
    props: ['course'],
    template: `
        <div style='border: 5px #1abc9c solid; text-align: center;'>
            {{ course }}
            <button type="button" 
                v-on:click="$emit('remove-course', course)"
                class="btn btn-danger btn-sm"
            >
                刪
            </button>
        </div> 
    `
}

var courseTable = {
    props: ['select_c'],
    data: function(){
        return {
            'courses': {},
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
            for(var c of this.select_c){
                this.courses[c.time] = c.name
            }
        }
    },
    components: {
        'course-div': courseDiv
    },
    template: `
<table class="table table-bordered">
    <thead>
        <th scope="col" class="col-md-1">#</th>
        <th scope="col" class="col-md-2">一</th>
        <th scope="col" class="col-md-2">二</th>
        <th scope="col" class="col-md-2">三</th>
        <th scope="col" class="col-md-2">四</th>
        <th scope="col" class="col-md-2">五</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="hour in 13">
            <template v-if="hour+7==12">
                <th style='text-align: center;' scope='row'>
                    {{ hour+7 }}~{{ hour+8 }}  <br> z
                </th>
                <td style='text-align: center; background-color: #1abc9c;' colspan='5'>
                    中午休息時間
                </td>
            </template>
            <template v-else>
                <th style='text-align: center;' scope='row'>
                    {{ hour+7 }} ~ {{ hour+8 }}   <br>
                    {{ String.fromCharCode(97+((hour<5)?(hour-1):(hour-2))) }}
                </th>
                <td v-for='week in 5'>
                    <course-div 
                        v-if="exist(week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2))))"
                        v-bind:course="courses[week+String.fromCharCode(97+((hour<5)?(hour-1):(hour-2)))]"
                        v-on:remove-course="removeCourseHandler"
                    ></course-div>
                </td>
            </template>
        </tr>
    </tbody>
</table>
    `
}