var coursesList = {
    props: ['courses', 'selected_d', 'selected_c', 'find_name'],
    data: function () {
        return {
            selectedTime: [],
            selectedId: [],
            foundedCourses: []
        }
    },
    methods: {
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
        'isOK': function (course) {
            var time = this.getTime(course.time)
            // console.log(course.name, " ", time)
            const isConflict = time.some((t) => this.selectedTime.includes(t))
            const isSelected = this.selectedId.includes((course.number+course.class))

            return !isConflict && !isSelected
        },
        'log': function (name, data) {
            console.log(name, data)
        }
    },
    watch: {
        'selected_c': function () {
            var timeTemp = []
            var idTemp = []
            for (var c of this.selected_c) {
                if (c.temp == false) {
                    timeTemp.push(c.time)
                    idTemp.push(c.number+c.class)
                }
            }
            this.selectedTime = timeTemp
            this.selectedId = idTemp
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
