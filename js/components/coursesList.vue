var coursesList = {
    props: ['courses', 'selected_d', 'selected_c', 'find_name'],
    data: function () {
        return {
            selectedTime: [],
            foundedCourses: []
        }
    },
    methods: {
        'getTime': function (timeString) {
            if (timeString == null) {
                return ""
            }

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
        'isOK': function (course) {
            var time = this.getTime(course.time)
            // console.log(course.name, " ", time)
            for (t of time) {
                for (st of this.selectedTime) {
                    if (t == st)
                        return false
                }
            }
            return true
        },
        'log': function (name, data) {
            console.log(name, data)
        }
    },
    watch: {
        'selected_c': function () {
            var temp = []
            for (var c of this.selected_c) {
                if (c.temp == false) {
                    temp.push(c.time)
                }
            }
            this.selectedTime = temp
        },
        'find_name': function () {
            const target = this.find_name.toLowerCase();
            this.foundedCourses = this.courses.filter((c) => c.name.toLowerCase().includes(target));
        }
    },
    template: `
    <div class="mx-auto mb-4">
		<h5>2. 安排課程</h5>
		<p style="color: orange" v-if="find_name"> ※ 已套用「名稱」搜尋： <br>{{find_name}}</p>
		<div style="width:275px;height:500px;overflow:auto">
			<table class="table table-striped table-bordered">
				<template v-if="find_name">
                    <tr v-for="(course, index) in foundedCourses" :key="index"
                    v-on:mouseenter="$emit('show-temp', course)" v-on:mouseleave="$emit('delete-temp', course)">
						<td>
							<div class="container row py-2 px-0">
								<div class="col-12 pr-1">
									<b>{{ course.name }} (<a v-bind:href="course.link" target="_blank">詳</a>)</b>
									—— {{ (course.department.indexOf(', ')!=-1) ?(course.department.split(', ')[1]) :(course.department) }}
								</div>
								<div class="col-sm-8 pr-1">
									{{ course.teacher }} ‧ {{ course.time }} 
								</div>
								<div class="col-sm-4 pr-1">
								    <button v-if="isOK(course)" type="button" v-on:click="$emit('add-course', course)" class="btn btn-primary">
										<span>&#43;</span>
									</button>
								</div>
							</div>
						</td>
					</tr>
				</template>
				<template v-else>
					<tr v-for="(course, index) in courses" :key="index"
                        v-if="course.department == selected_d"
                        v-on:mouseenter="$emit('show-temp', course)" v-on:mouseleave="$emit('delete-temp', course)">
						<td>
                        <div class="container row py-2 px-0">
                            <div class="col-12 pr-1">
                                <b>{{ course.name }} (<a v-bind:href="course.link" target="_blank">詳</a>)</b>
                            </div>
                            <div class="col-sm-8 pr-1">
                                {{ course.teacher }} ‧ {{ course.time }} 
                            </div>
                            <div class="col-sm-4 pr-1">
                                <button v-if="isOK(course)" type="button" v-on:click="$emit('add-course', course)" class="btn btn-primary">
                                    <span>&#43;</span>
                                </button>
                            </div>
                        </div>
						</td>
					</tr>
				</template>
			</table>
		</div>
    </div>
    `
}
