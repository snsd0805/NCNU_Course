var selectCourse = {
    props: ['course'],
    template: `
        <div style='border: 5px #1abc9c solid; text-align: center;'>
            {{ course.name }}
            <button 
                type="button" 
                v-on:click="$emit('remove-course', course)"
                class="btn btn-danger btn-sm"
            >
                刪
            </button>
        </div>
    `
}